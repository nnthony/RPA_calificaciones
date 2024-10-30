def eliminar_mayor_menor(num):
    # Variables para almacenar el número modificado
    resultado = 0
    factor = 1  # Se usa para colocar los dígitos en la posición correcta
    
    # Encontrar el mayor y menor dígito
    mayor = -1
    menor = 10
    temp = num
    
    while temp > 0:
        digito = temp % 10
        if digito > mayor:
            mayor = digito
        if digito < menor:
            menor = digito
        temp //= 10
    
    # Eliminar el mayor y menor dígito y construir el número modificado
    temp = num
    while temp > 0:
        digito = temp % 10
        if digito != mayor and digito != menor:
            resultado += digito * factor
            factor *= 10
        temp //= 10
    
    return resultado

# Programa principal
numero = int(input("Ingrese un número entero positivo (más de 4 dígitos): "))

if numero > 9999:  # Asegurarse de que el número tenga más de 4 dígitos
    numero_modificado = eliminar_mayor_menor(numero)
    print("Número modificado:", numero_modificado)
else:
    print("El número debe tener más de 4 dígitos.")
