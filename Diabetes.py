
# PERCEPTRON SIMPLE - DIABETES
# Entradas: IMC y Glucosa
# Salida: 0 = Sin diabetes, 1 = Con diabetes

import pandas as pd
import numpy as np
from pathlib import Path

# Leer archivo CSV desde la carpeta del programa
RUTA = Path(__file__).with_name("Diabetes_102_registros.csv")

df = pd.read_csv(RUTA)

# Columnas: IMC, Glucosa, Diabetes
df = df[["IMC", "Glucosa", "Diabetes"]].copy()

for columna in df.columns:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

df = df.dropna().reset_index(drop=True)

# Normalizacion
# X0 = 1
# X1 = IMC / 10
# X2 = Glucosa / 100

X = np.column_stack([
    np.ones(len(df)),
    df["IMC"].to_numpy() / 10.0,
    df["Glucosa"].to_numpy() / 100.0
])

y = df["Diabetes"].to_numpy(dtype=int)

# Configuracion del perceptron
W = np.zeros(3, dtype=float)
tasa = 0.1
max_epocas = 1000

print("=================================")
print(" PERCEPTRON SIMPLE - DIABETES")
print("=================================")

print("Registros:", len(df))

# Entrenamiento
for epoca in range(1, max_epocas + 1):

    errores = 0

    for xi, deseado in zip(X, y):

        Z = np.dot(W, xi)

        salida = int(Z >= 0)

        error = deseado - salida

        if error != 0:
            W += tasa * error * xi
            errores += 1

    print(f"Epoca {epoca}: errores = {errores}")

    if errores == 0:
        break

# Evaluacion sobre los registros de entrenamiento
predicciones = (X @ W >= 0).astype(int)

aciertos = int(np.sum(predicciones == y))
exactitud = 100 * aciertos / len(y)

print("\nRESULTADOS")

print(f"W0 = {W[0]:.6f}")
print(f"W1 = {W[1]:.6f}")
print(f"W2 = {W[2]:.6f}")

print(f"\nAciertos: {aciertos}/{len(y)}")
print(f"Exactitud: {exactitud:.2f}%")

print("\nECUACION:")
print(
    "Z = W0 + W1*(IMC/10) + W2*(Glucosa/100)"
)

print("Y = 1 si Z >= 0; de lo contrario Y = 0")

print("\nNota: exactitud sobre entrenamiento.")
print("No constituye un diagnostico medico.")
