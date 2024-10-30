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
    # Cargar los archivos .py y realizar la ejecución de los códigos
    files = os.listdir(app.config['EVAL_FOLDER'])

    results = {}
    for file in files:
        if file.endswith('.py'):
            student_id = file.split('.')[0]  # Obtener el ID del alumno a partir del nombre del archivo
            exercise_num = int(request.form.get('exercise_number'))  # Ejercicio correspondiente
            evaluations = extract_evaluation_data(exercise_num)
            if 't_evaluacion' in session: # Recuperar el valor de la evaluación
                t_evaluacion = session['t_evaluacion']
            # Ejecutar el archivo .py del alumno
            result = execute_code(file)
            results[student_id] = result
            print(result)

            insertar_eval(evaluations,exercise_num,result, student_id,file, t_evaluacion)

    flash('Calificaciones procesadas.')
    return redirect(url_for('index'))

# Analisis de plagio con jplag

@app.route('/run_jplag', methods=['POST'])
def run_jplag():
    if 't_evaluacion' in session:  # Verifica si t_evaluacion está en la sesión
        t_evaluacion = session['t_evaluacion']
    
    results = []  # Lista para almacenar los resultados de cada ejercicio

    # Definir las carpetas a analizar
    for i in range(1, 4):  # Para ejercicios 1, 2 y 3
        command = [
            'java', '-jar', 'jplag.jar', 
            '-l', 'python3', 
            '-s', f'./eval/{t_evaluacion}/{i}/', 
            '-r', f'./eval/{t_evaluacion}/eval-results-{i}/'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout  # Salida del comando
        
        # Crear una lista para almacenar los resultados formateados para este ejercicio
        comparisons = []
        lines = output.splitlines()
        
        for line in lines:
            if "Comparing" in line:
                parts = line.split(":")
                comparison = parts[0].replace("Comparing ", "").strip()
                percentage = float(parts[1].strip())
                
                if percentage > 0:
                    comparisons.append(f"Análisis entre {comparison}: {percentage:.1f}%")

        results.append(comparisons)  # Agregar los resultados de este ejercicio

    return render_template('index.html', results=results, t_evaluacion=t_evaluacion)



# Ruta para manejar la solicitud POST y activar el proceso de insercion de calificaciones
@app.route('/insertar_calificaciones', methods=['POST'])
def insertar_calificaciones_ruta():

    if 't_evaluacion' in session:  # Verifica si t_evaluacion está en la sesión
        t_evaluacion = session['t_evaluacion']  # Recupera la evaluación guardada
        insertar_calificaciones(t_evaluacion)  # Llama a la función de inserción
        flash(f"Se insertó correctamente las notas de {t_evaluacion}")
        return redirect(url_for('index'))  # Redirige a la página principal
    else:
        return "Error: No se encontró la evaluación en la sesión", 400  # Si no está en la sesión, muestra error

@app.route('/analisis',methods=['POST'])
def analisis():
    if 't_evaluacion' in session:  # Verifica si t_evaluacion está en la sesión
        t_evaluacion = session['t_evaluacion']
    
    numero_ejercicio = request.form.get('numero_ejercicio')
    if not numero_ejercicio:
        flash("Por favor, ingresa el número de ejercicio.")
        return redirect(url_for('index'))
    detalle = detalle_ej(t_evaluacion,numero_ejercicio)
    session['detalle'] = detalle
    if 'calificaciones' in session:
        calificaciones = session['calificaciones']
        return render_template('index.html', detalle=detalle, t_evaluacion=t_evaluacion, numero_ejercicio=numero_ejercicio, calificaciones=calificaciones)
    else:
        return render_template('index.html', detalle=detalle, t_evaluacion=t_evaluacion, numero_ejercicio=numero_ejercicio)

    


@app.route('/calificaciones', methods=['POST'])
def mostrar_calificaciones():
    if 't_evaluacion' in session:
        t_evaluacion = session['t_evaluacion']
    else:
        return "Evaluación no especificada en la sesión", 400  # Error si no está en sesión
    
    calificaciones = m_calificaciones(t_evaluacion)
    session['calificaciones'] = calificaciones
    if 'detalle' in session:
        detalle = session['detalle']
        return render_template('index.html', calificaciones=calificaciones, t_evaluacion=t_evaluacion, detalle=detalle)
    else:
        return render_template('index.html', calificaciones=calificaciones, t_evaluacion=t_evaluacion)

if __name__ == '__main__':
    app.run(debug=True)