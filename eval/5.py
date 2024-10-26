# Inicializar variables
n = int(input("Ingrese la cantidad de notas: "))
menor_nota = float('inf')
veces_repite = 0
numero_formado = 0
posicion_actual = 1  # Contador para las posiciones

# Se utilizará un ciclo for para iterar sobre la cantidad de notas
for _ in range(n):
    nota = int(input("Ingrese la nota: "))
    
    # Comparar la nota ingresada con la menor nota encontrada hasta ahora
    if nota < menor_nota:
        menor_nota = nota
        veces_repite = 1
        numero_formado = posicion_actual  # Reiniciar número formado con la nueva posición
    elif nota == menor_nota:
        veces_repite += 1
        # Formar el número con la nueva posición
        numero_formado = numero_formado * 10 + posicion_actual  # Agregar posición al número

    # Incrementar la posición
    posicion_actual += 1

# Imprimir resultados
print("Menor nota:", menor_nota)
print("Veces que se repite:", veces_repite)
print("Numero formado por las posiciones en que ocurre:", numero_formado)
