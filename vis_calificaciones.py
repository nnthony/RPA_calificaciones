from flask import render_template
from config import init_mysql
from app import app  # Importa la instancia de Flask


# Configuración inicial de la aplicación Flask

# Inicializar MySQL
mysql = init_mysql(app)

def m_calificaciones(t_evaluacion):
    cur = mysql.connection.cursor()
    query = """
    SELECT alumnos.id, alumnos.nombre_completo, alumnos.correo, 
           calificaciones.ejercicio1, 
           calificaciones.ejercicio2, calificaciones.ejercicio3, 
           calificaciones.nota_total
    FROM calificaciones
    JOIN alumnos ON calificaciones.id_alumno = alumnos.id
    WHERE calificaciones.evaluacion = %s
    """
    cur.execute(query, (t_evaluacion,))  # Pasa t_evaluacion como una tupla
    calificaciones = cur.fetchall()
    cur.close()
    return calificaciones