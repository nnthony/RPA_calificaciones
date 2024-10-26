# Inicializar variables
n = int(input("Ingrese la cantidad de notas: "))
menor_nota = float('inf')
veces_repite = 0
numero_formado = 0  # Usaremos un entero para formar el número

for i in range(1, n + 1):  # Comenzamos desde 1 para facilitar el conteo de posiciones
    nota = int(input("Ingrese la nota: "))
    
    if nota < menor_nota:
        menor_nota = nota
        veces_repite = 1
        numero_formado = i  # Reiniciar el número con la nueva posición
    elif nota == menor_nota:
        veces_repite += 1
        # Formar el número añadiendo la nueva posición
        numero_formado = numero_formado * 10 + i  # Desplazar los dígitos a la izquierda y añadir la posición

# Imprimir resultados
print("Menor nota:", menor_nota)
print("Veces que se repite:", veces_repite)
print("Numero formado por las posiciones en que ocurre:", numero_formado)
