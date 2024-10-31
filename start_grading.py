from flask import Flask, session
from config import *
import os, time, json
import subprocess
import openai

app = Flask(__name__)
mysql = init_mysql(app)

# Carpeta para cargar archivos
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
EVAL_FOLDER = 'eval/'
app.config['EVAL_FOLDER'] = EVAL_FOLDER


def execute_code(filename):
    """Función que ejecuta el código del alumno y captura el resultado"""
    filepath = os.path.join(app.config['EVAL_FOLDER'], filename)
    try:
        result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=10)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Tiempo excedido"
    except Exception as e:
        return f"Error en la ejecución del script: {e}"

def extract_evaluation_data(exercise_num):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT numero_ejercicio, enunciado, solucion FROM evaluaciones WHERE numero_ejercicio={exercise_num}")
    evaluations = cursor.fetchall()
    cursor.close()
    return evaluations

def almacenar_resultados(script):
    cur = mysql.connection.cursor()
    # Consulta SQL para insertar los resultados
    query = script
    # Ejecutar la consulta
    cur.execute(query)
    mysql.connection.commit()
    cur.close()

def insertar_eval(evaluations,exercise_num,result, student_id,file, t_evaluacion):
    for numero_ejercicio, enunciado, solucion in evaluations:
                if numero_ejercicio == exercise_num:
                    dir = f'eval/{t_evaluacion}/{exercise_num}/'
                    file_path = os.path.join(dir, file)
                    with open(file_path, 'r') as f:
                        # Lee todo el contenido del archivo
                            contenido = f.read()
                            contenido = str(contenido).replace("'", "\\'").replace("\n", "\\n")
                    # Evalúa la salida del código del estudiante
                    
                    if result == "Error" in result:
                        script = f"INSERT INTO detalle (id_alumno, eval ,numero_ejercicio, respuesta, C1, C2, C3, Total, comentario) VALUES ({student_id}, '{t_evaluacion}', {numero_ejercicio}, '{contenido}' ,0, 0, 0, 0, 'Este código no se ejecuta correctamente')"
                    else:
                        response = openai.ChatCompletion.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": f"Eres un docente del curso de algoritmia y estructura de datos, a continuación, se te dará el enunciado de un ejercicio en python y la respuesta de un estudiante, calificas con criterios de Correctitud/Funcionamiento (60%), Eficiencia (25%), Legibilidad(15%), considerando que C1: Correctitu y funcionamiento, C2: Eficiencia, C3: Legibilidad; y tu calificación irá a una base de datos, el formato de tu respuesta debe ser este script SQL (los valores de c1, C2, C3, deben ser decimales que representen al porcentaje, osea empiecen por 0. ;el valor de -respuesta- debe ser en formato texto y el valor de -Total- es la suma de todos los criterios; si el alumno no tiene respuesta, colocar a todos los criterios 0; envia el texto puro, no formatees en markdown; el valor de comentario debe ser el feedback breve para el alumno del porqué asignas las calificaciones por cada criterio): INSERT INTO detalle (id_alumno, eval ,numero_ejercicio, respuesta, C1, C2, C3, Total, comentario) VALUES ({student_id}, '{t_evaluacion}', {numero_ejercicio}, '{contenido}',0._, 0._, 0._, _, )"},
                                {"role": "user", "content": f"Enunciado del ejercicio: {enunciado}, Solucion del docente: {solucion}, Respuesta del alumno: {contenido}"}
                            ]
                        )
                        script = response['choices'][0]['message']['content']

                        # Define la ruta de la carpeta 'respuestas_IA' al mismo nivel que el código
                        respuestas_ia_folder = os.path.join(os.path.dirname(__file__), 'respuestas_IA')

                        # Asegúrate de que la carpeta 'respuestas_IA' existe, si no, la crea
                        if not os.path.exists(respuestas_ia_folder):
                            os.makedirs(respuestas_ia_folder)

                        # Genera un nombre de archivo único usando una marca de tiempo
                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                        json_file_path = os.path.join(respuestas_ia_folder, f"respuesta_{student_id}_{t_evaluacion}_{numero_ejercicio}_{timestamp}.json")

                        # Guarda la respuesta de OpenAI en un archivo JSON
                        with open(json_file_path, 'w') as json_file:
                            json.dump(response, json_file, indent=4)
                    # Retorna el puntaje calculado
                    almacenar_resultados(script)
                    print("8)")

def grade_exercises(t_evaluacion):
    results = {}
    for exercise_num in range(1, 4):
        dir = f'eval/{t_evaluacion}/{exercise_num}/'
        files = os.listdir(dir)
        for file in files:
            if file.endswith('.py'):
                student_id = file.split('.')[0]  # Obtener el ID del alumno a partir del nombre del archivo
                # Suponiendo que tienes funciones `extract_evaluation_data` y `execute_code` ya definidas
                evaluations = extract_evaluation_data(exercise_num)
                result = execute_code(file)
                results[student_id] = result
                # Llama a insertar_eval para guardar los resultados en la base de datos
                insertar_eval(evaluations, exercise_num, result, student_id, file, t_evaluacion)
    return results

def run_plagiarism_check(t_evaluacion):
    plagiarism_results = []
    for i in range(1, 4):  # Para ejercicios 1, 2 y 3
        command = [
            'java', '-jar', 'jplag.jar',
            '-l', 'python3',
            '-s', f'./eval/{t_evaluacion}/{i}/',
            '-r', f'./eval/{t_evaluacion}/eval-results-{i}/'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout

        # Procesar los resultados de comparación
        comparisons = []
        lines = output.splitlines()
        for line in lines:
            if "Comparing" in line:
                parts = line.split(":")
                comparison = parts[0].replace("Comparing ", "").strip()
                percentage = float(parts[1].strip())
                if percentage > 0:
                    comparisons.append(f"Análisis entre {comparison}: {percentage:.1f}%")

        plagiarism_results.append(comparisons)

    return plagiarism_results