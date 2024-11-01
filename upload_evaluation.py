from flask import Flask
from config import *
import pytesseract
from PIL import Image

app = Flask(__name__)
mysql = init_mysql(app)

def extract_text_from_image(file_path):
    #Extrae el texto del enunciado de una imagen usando Tesseract OCR.
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' ###Dirección local
    #el archivo tesseract.exe ejecuta el programa Tesseract en el equipo local
    return pytesseract.image_to_string(Image.open(file_path))

def store_evaluation_data(evals, enunciados, puntos ,soluciones):
    #Almacena los enunciados y soluciones procesados en la base de datos.
    cursor = mysql.connection.cursor()
    print("consulta SQL")
    for i, (eval, enunciado, punto ,solucion) in enumerate(zip(evals,enunciados, puntos ,soluciones)):
        query = """
        INSERT INTO evaluaciones (eval, numero_ejercicio, enunciado, puntos, solucion)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (eval, i+1, enunciado, punto, solucion))
    
    mysql.connection.commit()
    cursor.close()