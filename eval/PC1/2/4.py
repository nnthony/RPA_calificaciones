def eliminar_mayor_menor_alt(num):
    # Inicializamos variables
    mayor = -1
    menor = 10
    resultado = 0
    factor = 1
    original = num

    # Encontrar el mayor y menor dígito en una sola pasada
    while num > 0:
        digito = num % 10
        if digito > mayor:
            mayor = digito
        if digito < menor:
            menor = digito
        num //= 10

    # Resetear num para la segunda pasada
    num = original

    # Eliminar el mayor y menor dígito
    while num > 0:
        digito = num % 10
        # Si el dígito no es el mayor o menor, se agrega al resultado
        if digito != mayor and digito != menor:
            resultado = resultado + digito * factor
            factor *= 10
        num //= 10

    return resultado

# Programa principal
numero = int(input("Ingrese un número entero positivo (más de 4 dígitos): "))

if numero > 9999:  # Verificar que el número tenga más de 4 dígitos
    numero_modificado = eliminar_mayor_menor_alt(numero)
    print("Número modificado:", numero_modificado)
else:
    print("El número debe tener más de 4 dígitos.")
