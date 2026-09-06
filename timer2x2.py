import time

import time

a = int(input('valor de a: '))
b = int(input('valor de b: '))
c = int(input('valor de c: '))
d = int(input('valor de d: '))
e = int(input('valor de e: '))
f = int(input('valor de f: '))

tiempo_inicio = time.perf_counter()
x = (c/a)-(b/a)*(((f*a)-(d*c))/((e*a)-(d*b)))
y = (f*a-d*c)/(e*a-d*b)
tiempo_fin = time.perf_counter()

print(f'el valor de x es:{x}')
print(f'el valor de y es:{y}')
print(f'\nTiempo de cálculo: {tiempo_fin - tiempo_inicio:.9f} segundos')