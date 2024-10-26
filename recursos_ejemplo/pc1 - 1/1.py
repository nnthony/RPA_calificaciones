def sumar_base8(num1, num2):
    resultado = 0
    potencia = 1
    acarreo = 0

    while num1 > 0 or num2 > 0 or acarreo > 0:
        digito1 = num1 % 10
        digito2 = num2 % 10
        suma_digitos = digito1 + digito2 + acarreo

        if suma_digitos >= 8:
            acarreo = 1
            suma_digitos -= 8
        else:
            acarreo = 0

        resultado += suma_digitos * potencia
        potencia *= 10
        num1 //= 10
        num2 //= 10

    return resultado

def es_capicua(numero):
    original = numero
    invertido = 0

    while numero > 0:
        invertido = invertido * 10 + numero % 10
        numero //= 10

    return original == invertido

# Ejemplos de uso
num1 = 575  # en base 8
num2 = 636  # en base 8

resultado = sumar_base8(num1, num2)
print(f"Resultado de la suma en base 8: {resultado}")

if es_capicua(resultado):
    print(f"{resultado} es capicúa en base 8")
else:
    print(f"{resultado} no es capicúa en base 8")
