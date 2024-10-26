import os
import json

def calcular_promedio_tokens(carpeta_json):
    lista_tokens = []  # Lista para almacenar los valores de total_tokens
    
    # Recorre todos los archivos en la carpeta
    for archivo in os.listdir(carpeta_json):
        if archivo.endswith('.json'):
            # Abre cada archivo JSON
            with open(os.path.join(carpeta_json, archivo), 'r') as f:
                datos = json.load(f)
                # Almacena el valor de "total_tokens" en la lista
                lista_tokens.append(datos['usage']['total_tokens'])
    
    # Calcula el promedio si la lista no está vacía
    if lista_tokens:
        promedio = sum(lista_tokens) / len(lista_tokens)
        return promedio, lista_tokens  # Devuelve el promedio y la lista
    else:
        return 0, []  # Si no hay archivos o tokens

# Ruta de la carpeta donde están los archivos JSON
carpeta_json = r'C:\Users\antho\anaconda3\aData\rpa_calificaciones\respuestas_IA'

# Llamada a la función
promedio_tokens, lista_tokens = calcular_promedio_tokens(carpeta_json)

print(f"El promedio de 'total_tokens' es: {promedio_tokens}\nLa cantidad de respuestas es: {len(lista_tokens)}")

print(f"Lista de 'total_tokens': {lista_tokens}")