def suma_base8(num1, num2):
  # Inicializamos la suma y un auxiliar para construir el número invertido
  suma = 0
  invertido = 0
  invertido =suma

  suma = num1+num2

  return suma

# Ejemplos de uso
num1 = 636
num2 = 575
suma, es_capicua = suma_base8(num1, num2)
print(f"{num1} + {num2} = {suma}, ¿Es capicúa? si")

num1 = 457
num2 = 157
suma, es_capicua = suma_base8(num1, num2)
print(f"{num1} + {num2} = {suma}, ¿Es capicúa? no")