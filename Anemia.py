
"""Practica academica: perceptron simple con 4 entradas para Anemia.
Instalar: pip install pandas numpy matplotlib
Colocar Anemia (1).csv en la misma carpeta que este script.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ARCHIVO = Path(__file__).with_name('Anemia (1).csv')
TASA = 0.1
MAX_EPOCAS = 1000
COLUMNAS = ['Edad', 'Energia', 'Frecuencia', 'Antecedentes', 'Anemia']

# 1. Leer y limpiar el archivo original
original = pd.read_csv(ARCHIVO)
if not set(COLUMNAS).issubset(original.columns):
    raise ValueError(
        f'Columnas requeridas: {COLUMNAS}. '
        f'Encontradas: {list(original.columns)}'
    )

df = original[COLUMNAS].copy()

for columna in COLUMNAS:
    df[columna] = pd.to_numeric(df[columna], errors='coerce')

df = df.dropna().reset_index(drop=True)

if not df['Anemia'].isin([0, 1]).all() or not df['Antecedentes'].isin([0, 1]).all():
    raise ValueError('Anemia y Antecedentes deben contener solamente 0 o 1.')

print(f'Filas originales: {len(original)} | Registros validos: {len(df)}')
print('Clases:', df['Anemia'].value_counts().sort_index().to_dict())

if (df['Antecedentes'] == df['Anemia']).all():
    print('ADVERTENCIA: Antecedentes coincide exactamente con Anemia en todo el archivo.')
    print('La exactitud puede ser artificialmente alta por fuga de informacion.')

# 2. Escalamiento fijo
# X0=1, X1=Edad/100, X2=Energia/10,
# X3=Frecuencia/100, X4=Antecedentes

def entradas(edad, energia, frecuencia, antecedentes):
    return np.array([
        1.0,
        edad / 100.0,
        energia / 10.0,
        frecuencia / 100.0,
        antecedentes
    ], dtype=float)

X = np.array([
    entradas(*fila)
    for fila in df[
        ['Edad', 'Energia', 'Frecuencia', 'Antecedentes']
    ].to_numpy()
])

y = df['Anemia'].to_numpy(dtype=int)

# 3. Entrenamiento secuencial del perceptron

W = np.zeros(5, dtype=float)
historial = []

for epoca in range(1, MAX_EPOCAS + 1):

    errores = 0

    for xi, esperado in zip(X, y):

        z = float(np.dot(W, xi))
        obtenido = int(z >= 0)
        error = int(esperado) - obtenido

        if error != 0:
            W += TASA * error * xi
            errores += 1

    pred = (X @ W >= 0).astype(int)
    exactitud = 100 * np.mean(pred == y)

    historial.append((epoca, errores, exactitud))

    print(
        f'Epoca {epoca:4d} | '
        f'errores durante entrenamiento: {errores:3d} | '
        f'exactitud: {exactitud:6.2f}%'
    )

    if errores == 0:
        break

# 4. Evaluacion sobre el dataset

pred = (X @ W >= 0).astype(int)
aciertos = int(np.sum(pred == y))

print('\nPESOS APRENDIDOS')

for i, peso in enumerate(W):
    print(f'W{i} = {peso:.8f}')

print(f'\nAciertos: {aciertos}/{len(y)}')

print(
    f'Exactitud en el dataset de entrenamiento: '
    f'{100 * aciertos / len(y):.2f}%'
)

print('Ecuacion:')

print(
    f'Z = {W[0]:+.8f} '
    f'{W[1]:+.8f}*(Edad/100) '
    f'{W[2]:+.8f}*(Energia/10) '
    f'{W[3]:+.8f}*(Frecuencia/100) '
    f'{W[4]:+.8f}*Antecedentes'
)

print('Y = 1 si Z >= 0; de lo contrario Y = 0')

# 5. Grafica de dispersion
# Cuatro entradas no pueden visualizarse
# completamente en un plano de dos dimensiones.

fig, ax = plt.subplots(figsize=(9, 6))

for clase, etiqueta in [
    (0, 'Sin anemia (0)'),
    (1, 'Con anemia (1)')
]:
    sub = df[df['Anemia'] == clase]

    ax.scatter(
        sub['Energia'],
        sub['Frecuencia'],
        label=etiqueta,
        alpha=0.8,
        s=40
    )

ax.set(
    xlabel='Energia',
    ylabel='Frecuencia',
    title='Anemia: proyeccion de dos de las cuatro entradas'
)

ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

fig.savefig(
    Path(__file__).with_name('Anemia_Dispersion.png'),
    dpi=200
)

# 6. Grafica de evolucion del entrenamiento

hist = np.array(historial)

fig2, ax2 = plt.subplots(figsize=(9, 5))

ax2.plot(
    hist[:, 0],
    hist[:, 2],
    marker='o'
)

ax2.set(
    xlabel='Epoca',
    ylabel='Exactitud (%)',
    title='Evolucion de la exactitud del perceptron',
    ylim=(0, 105)
)

ax2.grid(alpha=0.25)
fig2.tight_layout()

fig2.savefig(
    Path(__file__).with_name('Anemia_Entrenamiento.png'),
    dpi=200
)

plt.show()

# 7. Prediccion interactiva

print('\nPRUEBA DE UN NUEVO REGISTRO')
print('Presiona Enter sin escribir nada para salir.')

while True:

    try:
        texto = input('Edad (Enter para salir): ').strip()

        if not texto:
            break

        edad = float(texto)
        energia = float(input('Energia: '))
        frecuencia = float(input('Frecuencia: '))
        antecedentes = float(
            input('Antecedentes (0 o 1): ')
        )

        if (
            edad <= 0 or
            energia < 0 or
            frecuencia <= 0 or
            antecedentes not in (0, 1)
        ):
            print('Valores invalidos. Intenta de nuevo.')
            continue

        xi = entradas(
            edad,
            energia,
            frecuencia,
            antecedentes
        )

        z = float(W @ xi)
        salida = int(z >= 0)

        print(f'\nSuma ponderada Z = {z:.8f}')
        print(f'Salida de la red Y = {salida}')

        if salida == 1:
            print('Clasificacion del modelo: CON ANEMIA')
        else:
            print('Clasificacion del modelo: SIN ANEMIA')

        print('Resultado academico, no diagnostico medico.\n')

    except ValueError:
        print('Introduce valores numericos validos.')

    except (EOFError, KeyboardInterrupt):
        break
