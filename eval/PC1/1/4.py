def suma_base8(num1, num2):
  # Inicializamos la suma y un auxiliar para construir el número invertido
  suma = 0
  invertido = 0

  # Realizamos la suma digit a digit, similar a como lo haríamos a mano
  while num1 > 0 or num2 > 0:
    suma = (num1 % 10 + num2 % 10 + suma) % 8
    invertido = invertido * 10 + suma % 10
    num1 //= 10
    num2 //= 10

  # Descartamos los ceros a la izquierda del número invertido
  while invertido % 10 == 0:
    invertido //= 10

  # Comparamos el número con su inverso para determinar si es capicúa
  es_capicua = suma == invertido

  return suma, es_capicua

# Ejemplos de uso
num1 = 636
num2 = 575
suma, es_capicua = suma_base8(num1, num2)
print(f"{num1} + {num2} = {suma}, ¿Es capicúa? {es_capicua}")

num1 = 457
num2 = 157
suma, es_capicua = suma_base8(num1, num2)
print(f"{num1} + {num2} = {suma}, ¿Es capicúa? {es_capicua}")