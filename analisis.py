from flask import render_template
from config import init_mysql
from app import app  # Importa la instancia de Flask


# Configuración inicial de la aplicación Flask

# Inicializar MySQL
mysql = init_mysql(app)

def detalle_ej(t_evaluacion):
    detalle=[]
    for numero_ejercicio in range(1,4):
        cur = mysql.connection.cursor()
        query = """
        SELECT 
            d.id_alumno, 
            a.nombre_completo, 
            ROUND(d.C1 * e.puntos, 2) AS criterio1,
            ROUND(d.C2 * e.puntos, 2) AS criterio2,
            ROUND(d.C3 * e.puntos, 2) AS criterio3,
            ROUND(d.Total * e.puntos, 2) AS total
        FROM detalle d
        JOIN alumnos a ON d.id_alumno = a.id
        JOIN evaluaciones e ON d.eval = e.eval AND d.numero_ejercicio = e.numero_ejercicio
        WHERE d.eval = %s AND d.numero_ejercicio = %s;
        """
        cur.execute(query, (t_evaluacion,numero_ejercicio))  # Pasa t_evaluacion como una tupla
        detalle_u = cur.fetchall()
        cur.close()
        detalle.append(detalle_u)
    return detalle