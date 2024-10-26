from flask import Flask
from config import *

app = Flask(__name__)
mysql = init_mysql(app)

def insertar_calificaciones(evaluacion):
    conn = mysql.connection
    cursor = conn.cursor()

    # Obtener los alumnos
    query_alumnos = """
    SELECT DISTINCT id_alumno 
    FROM detalle 
    WHERE eval = %s
    """
    cursor.execute(query_alumnos, (evaluacion,))
    alumnos = cursor.fetchall()

    for alumno in alumnos:
        id_alumno = alumno[0]

        # Obtener detalles para los tres ejercicios
        for ejercicio in range(1, 4):
            query_detalle = """
            SELECT d.Total, e.puntos 
            FROM detalle d 
            JOIN evaluaciones e 
            ON d.eval = e.eval AND d.numero_ejercicio = e.numero_ejercicio 
            WHERE d.eval = %s 
            AND d.numero_ejercicio = %s 
            AND d.id_alumno = %s
            """
            cursor.execute(query_detalle, (evaluacion, ejercicio, id_alumno))
            detalle = cursor.fetchone()

            if detalle:
                total, puntos = detalle
                # Calcular el puntaje para el ejercicio
                puntaje_ejercicio = total * puntos
            else:
                puntaje_ejercicio = 0  # Si no existe, el puntaje es 0

            # Asignar puntajes por ejercicio a las variables
            if ejercicio == 1:
                ejercicio1 = puntaje_ejercicio
            elif ejercicio == 2:
                ejercicio2 = puntaje_ejercicio
            elif ejercicio == 3:
                ejercicio3 = puntaje_ejercicio

        # Calcular la nota total
        nota_total = ejercicio1 + ejercicio2 + ejercicio3

        # Insertar los valores en la tabla calificaciones
        query_insert_calificaciones = """
        INSERT INTO calificaciones (id_alumno, evaluacion, ejercicio1, ejercicio2, ejercicio3, nota_total)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert_calificaciones, (id_alumno, evaluacion, ejercicio1, ejercicio2, ejercicio3, nota_total))
        conn.commit()

    cursor.close()

