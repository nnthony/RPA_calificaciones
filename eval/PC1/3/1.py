def procesar_notas(n):
    menor_nota = float('inf')  # Inicializa con infinito para encontrar la menor nota
    contador = 0  # Contador de veces que ocurre la menor nota
    posiciones = 0  # Número que almacenará las posiciones donde ocurre la menor nota
    posicion_actual = 1  # Para rastrear la posición de las notas

    for _ in range(n):
        nota = int(input("Ingrese una nota: "))
        
        # Comprobar si la nota ingresada es menor que la menor nota encontrada
        if nota < menor_nota:
            menor_nota = nota
            contador = 1  # Reiniciar el contador
            posiciones = posicion_actual  # Reiniciar las posiciones
        elif nota == menor_nota:
            contador += 1  # Aumentar el contador de ocurrencias
            posiciones = posiciones * 10 + posicion_actual  # Agregar la nueva posición

        posicion_actual += 1  # Incrementar la posición

    # Resultados
    print("Menor nota:", menor_nota)
    print("Veces que se repite:", contador)
    print("Número formado por las posiciones en que ocurre:", posiciones)

# Leer el número de notas a ingresar
n = int(input("Ingrese el número de notas: "))
procesar_notas(n)
