def eliminar_mayor_menor_ineficiente(num):
    # Inicializamos variables redundantes
    mayor = -1
    menor = 10
    temp_num = num
    temp_mayor = 0
    temp_menor = 0
    factor = 1
    resultado = 0
    
    while temp_num > 0:
        digito = temp_num % 10
        
        temp_mayor = mayor
        temp_menor = menor
        
        if digito > mayor:
            mayor = digito
        if digito < menor:
            menor = digito
        
        for i in range(1):
            if digito != mayor and digito != menor:
                resultado += digito * factor
                factor *= 10
        
        temp_num //= 10
    
    resultado_temp = resultado
    final_resultado = 0
    factor_temp = 1
    
    while resultado_temp > 0:
        digito_final = resultado_temp % 10
        final_resultado += digito_final * factor_temp
        factor_temp *= 10
        resultado_temp //= 10

    return final_resultado

numero = int(input("Ingrese un número entero positivo (más de 4 dígitos): "))

if numero > 9999:  # Asegurarse de que el número tenga más de 4 dígitos
    mayor_digito = -1
    menor_digito = 10
    temp_check = numero
    
    while temp_check > 0:
        digito_check = temp_check % 10
        if digito_check > mayor_digito:
            mayor_digito = digito_check
        if digito_check < menor_digito:
            menor_digito = digito_check
        temp_check //= 10
    
    print("Mayor dígito:", mayor_digito)
    print("Menor dígito:", menor_digito)

    numero_modificado = eliminar_mayor_menor_ineficiente(numero)
    print("Número modificado:", numero_modificado)
else:
    print("El número debe tener más de 4 dígitos.")
