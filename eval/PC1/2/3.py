def eliminar_mayor_menor(num):
    resultado = 0
    factor = 1
    
    mayor = -1
    menor = 10
    temp = num
    
    resultado = temp - mayor*10 - menor*1000
    
    return resultado

# Programa principal
numero = int(input("Ingrese un número entero positivo (más de 4 dígitos): "))

if numero > 9999: 
    numero_modificado = eliminar_mayor_menor(numero)
    print("Número modificado:", numero_modificado)
else:
    print("El número debe tener más de 4 dígitos.")
