def suma_octal(a, b):
    # Función para sumar dos números en base 8 dígito por dígito
    acarreo = 0
    resultado = 0
    multiplicador = 1
    
    while a > 0 or b > 0 or acarreo > 0:
        digito_a = a % 10
        digito_b = b % 10
        
        suma_digitos = digito_a + digito_b + acarreo
        resultado_digito = suma_digitos % 8  # Módulo base 8
        acarreo = suma_digitos // 8  # Acarreo en base 8
        
        resultado += resultado_digito * multiplicador
        multiplicador *= 10
        
        a //= 10
        b //= 10
    
    return resultado

def es_capicua(numero):
    # Función para determinar si un número de tres dígitos es capicúa en base 8
    digito_1 = numero // 100
    digito_2 = (numero // 10) % 10
    digito_3 = numero % 10
    
    return digito_1 == digito_3  # Capicúa si el primer y último dígito son iguales

# Ejemplos
primer_numero = 575  # Número en base 8
segundo_numero = 636  # Número en base 8

resultado = suma_octal(primer_numero, segundo_numero)
print("Resultado de la suma en base 8:", resultado)

if es_capicua(resultado):
    print(f"{resultado} es capicúa en base 8")
else:
    print(f"{resultado} no es capicúa en base 8")
