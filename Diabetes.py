
# ============================================================
# PERCEPTRON SIMPLE - OBESIDAD
# 90% ENTRENAMIENTO / 10% EVALUACION
# ============================================================

# Instalar:
# pip install numpy pandas matplotlib

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# 1. CONFIGURACION
# ------------------------------------------------------------

RUTA = Path(__file__).with_name("Obesidad(1).csv")

COLUMNAS = [
    "Edad",
    "Sexo",
    "IMC",
    "Actividad",
    "Calorias",
    "Antecedentes",
    "Obesidad"
]

ESCALAS = np.array([
    100.0,    # Edad
    1.0,      # Sexo
    50.0,     # IMC
    10.0,     # Actividad
    5000.0,   # Calorias
    1.0       # Antecedentes
])

TASA = 0.1
SEMILLA = 42
MAX_EPOCAS = 1000


# ------------------------------------------------------------
# 2. LEER EL ARCHIVO CSV
# ------------------------------------------------------------

df = pd.read_csv(RUTA)

if not set(COLUMNAS).issubset(df.columns):
    raise ValueError(
        f"Columnas esperadas: {COLUMNAS}"
    )

df = (
    df[COLUMNAS]
    .apply(pd.to_numeric, errors="coerce")
    .dropna()
    .reset_index(drop=True)
)

for columna in ["Sexo", "Antecedentes", "Obesidad"]:

    if not df[columna].isin([0, 1]).all():
        raise ValueError(
            f"{columna} debe contener solamente 0 o 1"
        )


# ------------------------------------------------------------
# 3. PREPARAR LAS SEIS ENTRADAS
# ------------------------------------------------------------

valores = df[COLUMNAS[:-1]].to_numpy(dtype=float)

# X0 = 1 (entrada constante)
# X1 = Edad / 100
# X2 = Sexo
# X3 = IMC / 50
# X4 = Actividad / 10
# X5 = Calorias / 5000
# X6 = Antecedentes

X = np.column_stack([
    np.ones(len(df)),
    valores / ESCALAS
])

# Salida deseada:
# 0 = Sin obesidad
# 1 = Con obesidad

y = df["Obesidad"].to_numpy(dtype=int)


# ------------------------------------------------------------
# 4. DIVISION 90% / 10%
# ------------------------------------------------------------

# La division es estratificada:
# conserva aproximadamente la proporcion de cada clase.

rng = np.random.default_rng(SEMILLA)

train_idx = []
test_idx = []

for clase in (0, 1):

    indices = np.flatnonzero(y == clase)

    rng.shuffle(indices)

    n_test = round(len(indices) * 0.10)

    test_idx.extend(indices[:n_test])

    train_idx.extend(indices[n_test:])


train_idx = np.array(train_idx)

test_idx = np.array(test_idx)

rng.shuffle(train_idx)

rng.shuffle(test_idx)


print("=" * 55)
print("PERCEPTRON SIMPLE - OBESIDAD")
print("=" * 55)

print(f"Registros validos: {len(df)}")

print(f"Datos de entrenamiento: {len(train_idx)}")

print(f"Datos de evaluacion: {len(test_idx)}")


# ------------------------------------------------------------
# 5. ENTRENAMIENTO DEL PERCEPTRON
# ------------------------------------------------------------

# Siete pesos:
# W0, W1, W2, W3, W4, W5, W6

W = np.zeros(7, dtype=float)

historial = []

for epoca in range(1, MAX_EPOCAS + 1):

    errores = 0

    for i in train_idx:

        # Suma ponderada

        Z = np.dot(W, X[i])

        # Funcion de activacion escalon

        salida = int(Z >= 0)

        # Calcular error

        error = int(y[i]) - salida

        # Actualizacion de pesos

        if error != 0:

            W += TASA * error * X[i]

            errores += 1

    # Evaluar el conjunto de entrenamiento

    pred_train = (
        X[train_idx] @ W >= 0
    ).astype(int)

    exactitud_train = np.mean(
        pred_train == y[train_idx]
    )

    historial.append((
        epoca,
        errores,
        exactitud_train * 100
    ))

    print(
        f"Epoca {epoca}: "
        f"errores = {errores} | "
        f"exactitud = {exactitud_train:.2%}"
    )

    # Terminar cuando no existan errores de actualizacion

    if errores == 0:
        break


# ------------------------------------------------------------
# 6. EVALUACION CON EL 10% RESERVADO
# ------------------------------------------------------------

pred_train = (
    X[train_idx] @ W >= 0
).astype(int)

pred_test = (
    X[test_idx] @ W >= 0
).astype(int)

aciertos_train = np.sum(
    pred_train == y[train_idx]
)

aciertos_test = np.sum(
    pred_test == y[test_idx]
)

exactitud_train = (
    aciertos_train / len(train_idx)
) * 100

exactitud_test = (
    aciertos_test / len(test_idx)
) * 100


print("\n" + "=" * 55)
print("RESULTADOS DEL ENTRENAMIENTO Y EVALUACION")
print("=" * 55)

print(f"Epocas utilizadas: {epoca}")

print(
    f"Entrenamiento: "
    f"{aciertos_train}/{len(train_idx)}"
)

print(
    f"Exactitud entrenamiento: "
    f"{exactitud_train:.2f}%"
)

print(
    f"Evaluacion: "
    f"{aciertos_test}/{len(test_idx)}"
)

print(
    f"Exactitud evaluacion: "
    f"{exactitud_test:.2f}%"
)


# ------------------------------------------------------------
# 7. MOSTRAR LOS SIETE PESOS APRENDIDOS
# ------------------------------------------------------------

print("\nPESOS APRENDIDOS")

for j, peso in enumerate(W):

    print(f"W{j} = {peso:.8f}")


print("\nECUACION DEL PERCEPTRON")

print(
    "Z = W0 + W1*(Edad/100) + W2*Sexo "
    "+ W3*(IMC/50) + W4*(Actividad/10) "
    "+ W5*(Calorias/5000) + W6*Antecedentes"
)

print("Y = 1 si Z >= 0; en caso contrario Y = 0")


# ------------------------------------------------------------
# 8. GUARDAR LOS REGISTROS DE EVALUACION
# ------------------------------------------------------------

evaluacion = df.iloc[test_idx].copy()

evaluacion["Prediccion"] = pred_test

evaluacion["Correcto"] = (
    pred_test == y[test_idx]
).astype(int)

evaluacion.to_csv(
    Path(__file__).with_name(
        "Obesidad_Evaluacion_10.csv"
    ),
    index=False
)


# Guardar los pesos

pd.DataFrame({

    "Peso": [f"W{i}" for i in range(7)],

    "Valor": W

}).to_csv(

    Path(__file__).with_name("Obesidad_Pesos.csv"),

    index=False
)


# ------------------------------------------------------------
# 9. GRAFICA DE DISPERSION
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 5))

for clase, nombre in [
    (0, "Sin obesidad"),
    (1, "Con obesidad")
]:

    sub = df[df["Obesidad"] == clase]

    ax.scatter(
        sub["IMC"],
        sub["Calorias"],
        alpha=0.65,
        label=nombre
    )


ax.set_title("Obesidad: dispersion IMC vs calorias")

ax.set_xlabel("IMC")

ax.set_ylabel("Calorias")

ax.legend()

ax.grid(alpha=0.25)

fig.tight_layout()

fig.savefig(
    Path(__file__).with_name("Obesidad_Dispersion.png"),
    dpi=180
)


# ------------------------------------------------------------
# 10. GRAFICA DE ENTRENAMIENTO
# ------------------------------------------------------------

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.plot(

    [r[0] for r in historial],

    [r[2] for r in historial],

    marker="o"

)

ax2.set_title("Exactitud durante el entrenamiento")

ax2.set_xlabel("Epoca")

ax2.set_ylabel("Exactitud (%)")

ax2.set_ylim(0, 105)

ax2.grid(alpha=0.25)

fig2.tight_layout()

fig2.savefig(
    Path(__file__).with_name(
        "Obesidad_Entrenamiento.png"
    ),
    dpi=180
)

plt.show()


# ------------------------------------------------------------
# 11. OBSERVACIONES
# ------------------------------------------------------------

print("\nOBSERVACIONES:")

print(
    "La variable Antecedentes casi reproduce "
    "la etiqueta Obesidad."
)

print(
    "Existe riesgo de fuga de informacion."
)

print(
    "Este programa es exclusivamente academico "
    "y no constituye un diagnostico medico."
)
