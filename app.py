from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from config import Config, init_mysql
from insert_c import *
from upload_evaluation import *
from start_grading import *
from vis_calificaciones import *
from analisis import *
import os
import openai

# Configuración inicial de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)  # Cargar las configuraciones desde config.py

# Inicializar la API key de OpenAI
openai.api_key = app.config['OPENAI_API_KEY']

# Inicializar MySQL
mysql = init_mysql(app)
# Carpeta para cargar archivos
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
EVAL_FOLDER = 'eval/'
app.config['EVAL_FOLDER'] = EVAL_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'py', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página principal para seleccionar la evaluación
@app.route('/')
def index():
    if 't_evaluacion' in session:  # Verifica si t_evaluacion está en la sesión
        t_evaluacion = session['t_evaluacion']
        return render_template('index.html', t_evaluacion=t_evaluacion)
    else:
        return render_template('index.html')

# Ruta para guardar el tipo de evaluación en la sesión
@app.route('/set_evaluation_type', methods=['POST'])
def set_evaluation_type():
    
    t_evaluacion = request.form.get('t_evaluacion')
    session['t_evaluacion'] = t_evaluacion  # Guardar en sesión
    UPLOAD_FOLDER = f'uploads/{t_evaluacion}/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    EVAL_FOLDER = f'eval/{t_evaluacion}/'
    app.config['EVAL_FOLDER'] = EVAL_FOLDER
    print(session)
    flash("Se declaró correctamente el tipo de evaluación")
    return redirect(url_for('index'))  # Redirigir a una página, o donde prefieras

# Ruta para manejar la carga de la evaluación (imágenes de los ejercicios)
@app.route('/upload_evaluation', methods=['POST'])
def upload_evaluation():
    if 't_evaluacion' in session:  # Verifica si t_evaluacion está en la sesión
        t_evaluacion = session['t_evaluacion']
    if 'evaluation_images' not in request.files:
        flash('No se seleccionaron archivos')
        return redirect(request.url)

    files = request.files.getlist('evaluation_images')
    if not files:
        flash('No se seleccionaron archivos')
        return redirect(request.url)

    # Inicializar listas para almacenar enunciados y soluciones
    enunciados = []
    evals=[]
    puntos=[]
    soluciones = []
    
    # Procesar cada imagen y obtener enunciado y solución usando Tesseract y OpenAI
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            if 't_evaluacion' in session: # Recuperar el valor de la evaluación
                t_evaluacion = session['t_evaluacion']
            try:
                # Extraer el texto del enunciado de la imagen usando Tesseract
                enunciado = extract_text_from_image(file_path)
                enunciados.append(enunciado)
                evals.append(t_evaluacion)
                
                # Enviar el enunciado a la API de OpenAI para generar una solución
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": f"Resuelve el siguiente ejercicio en python, solo coloca el codigo, no le des formato markdown: {enunciado}"}
                    ],
                    max_tokens=500
                )
                
                solucion = response.choices[0].message['content'].strip()
                soluciones.append(solucion)

                # Enviar el enunciado a la API de OpenAI para generar una solución
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "user", "content": f"Este es el enunciado de un ejercicio en python, cuantos puntos vale? está al lado de la palabra 'pregunta -' generalmente. (solo responde la cifra): {enunciado}"}
                    ],
                    max_tokens=500
                )
                
                puntaje = response.choices[0].message['content'].strip()
                puntos.append(puntaje)

            except Exception as e:
                flash(f'Error al procesar la imagen {filename}: {str(e)}')
                print("ocurró un error")
                
    # Guardar las respuestas procesadas en la base de datos
    store_evaluation_data(evals, enunciados, puntos ,soluciones)
    flash('Evaluación cargada correctamente.')
    return redirect(url_for('index'))


# Ruta para manejar la carga de códigos de los alumnos
@app.route('/upload_codes', methods=['POST'])
def upload_codes():
    if 't_evaluacion' in session:
        t_evaluacion = session['t_evaluacion']

    # Diccionario para cada ejercicio y su respectiva lista de archivos
    exercises = {
        '1': request.files.getlist('code_files_1'),
        '2': request.files.getlist('code_files_2'),
        '3': request.files.getlist('code_files_3')
    }

    # Procesa cada conjunto de archivos
    for exercise_number, files in exercises.items():
        dir = f'eval/{t_evaluacion}/{exercise_number}/'
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(dir, filename))

    flash('Archivos subidos correctamente para todos los ejercicios.')
    return redirect(url_for('index'))



# Ruta para iniciar el proceso de calificación
@app.route('/start_grading', methods=['POST'])
def start_grading():
    if 't_evaluacion' in session:
        t_evaluacion = session['t_evaluacion']

        # Llamar a la función para calificar los ejercicios
        grade_exercises(t_evaluacion)
        flash('Calificaciones procesadas.')

        # Llamar a la función para el análisis de plagio
        plagiarism_results = run_plagiarism_check(t_evaluacion)

        # Llamar a la función para insertar calificaciones en la base de datos
        insertar_calificaciones(t_evaluacion)
        flash(f"Se insertaron correctamente las notas de {t_evaluacion} y se completó el análisis de plagio.")
        session['plagiarism_results']=plagiarism_results
        return render_template('index.html', plagiarism_results=plagiarism_results, t_evaluacion=t_evaluacion)
    else:
        flash("Error: No se encontró la evaluación en la sesión.")
        return redirect(url_for('index'))

@app.route('/analisis',methods=['POST'])
def analisis():
    if ('t_evaluacion' in session):  # Verifica si t_evaluacion está en la sesión
        t_evaluacion = session['t_evaluacion']
    if ('plagiarism_results' in session):
        plagiarism_results = session['plagiarism_results']
    
    
    detalle = detalle_ej(t_evaluacion)
    session['detalle'] = detalle

    calificaciones = m_calificaciones(t_evaluacion)
    session['calificaciones'] = calificaciones

    if 'calificaciones' in session and 'plagiarism_results' in session:
        return render_template('index.html', detalle=detalle, t_evaluacion=t_evaluacion, calificaciones=calificaciones, plagiarism_results=plagiarism_results)
    elif 'calificaciones' in session:
        calificaciones = session['calificaciones']
        return render_template('index.html', detalle=detalle, t_evaluacion=t_evaluacion, calificaciones=calificaciones)
    elif 'plagiarism_results' in session:
        return render_template('index.html', detalle=detalle, t_evaluacion=t_evaluacion, plagiarism_results=plagiarism_results)
    else:
        return render_template('index.html', detalle=detalle, t_evaluacion=t_evaluacion)



if __name__ == '__main__':
    app.run(debug=True)