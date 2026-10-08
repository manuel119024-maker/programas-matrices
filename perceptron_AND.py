
import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# PERCEPTRON PARA COMPUERTA LOGICA AND
# ==================================================

# 1. DATOS DE ENTRENAMIENTO

X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

Y = np.array([0, 0, 0, 1])

# 2. PARAMETROS DEL PERCEPTRON

np.random.seed(1)

pesos = np.random.uniform(-1, 1, 2)
bias = np.random.uniform(-1, 1)

alpha = 0.1
epocas = 100

historial_error = []

# 3. FUNCION DE ACTIVACION ESCALON

def activacion(z):
    return 1 if z >= 0 else 0

# 4. ENTRENAMIENTO

print("\n==========================================")
print("    ENTRENAMIENTO DEL PERCEPTRON AND")
print("==========================================")

for epoca in range(1, epocas + 1):

    error_total = 0

    for i in range(len(X)):

        # Suma ponderada
        z = np.dot(X[i], pesos) + bias

        # Salida calculada
        salida = activacion(z)

        # Error
        error = Y[i] - salida

        # Ajuste de pesos y bias
        pesos = pesos + alpha * error * X[i]
        bias = bias + alpha * error

        # Error cuadratico
        error_total += error ** 2

    # Error cuadratico medio
    mse = error_total / len(X)

    historial_error.append(mse)

    print(f"Epoca {epoca:3d} | Error = {mse:.6f}")

    # Detener cuando no existan errores
    if mse == 0:
        print("\nEl perceptron aprendio la compuerta AND.")
        break

# 5. RESULTADOS FINALES

print("\n==========================================")
print("             RESULTADOS")
print("==========================================")

print("\nPesos finales:", pesos)
print("Bias final:", bias)

print("\n X1  X2  Deseada  Obtenida")

for i in range(len(X)):

    z = np.dot(X[i], pesos) + bias
    salida = activacion(z)

    print(
        f" {X[i,0]}   {X[i,1]}      {Y[i]}        {salida}"
    )

print(f"\nError final: {historial_error[-1]:.6f}")
print(f"Epocas realizadas: {len(historial_error)}")

# 6. GRAFICA DEL ERROR

plt.figure(figsize=(10, 6))

plt.plot(
    range(1, len(historial_error) + 1),
    historial_error,
    marker="o",
    linewidth=2,
    label="Error cuadratico medio"
)

plt.xlabel("Epocas")
plt.ylabel("Error cuadratico medio (MSE)")
plt.title("Aprendizaje del perceptron - Compuerta AND")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# 7. GRAFICA DE LA COMPUERTA AND

fig, ax = plt.subplots(figsize=(7, 6))

for i in range(len(X)):

    color = "green" if Y[i] == 1 else "red"

    ax.scatter(
        X[i, 0],
        X[i, 1],
        color=color,
        s=180
    )

    ax.annotate(
        f"({X[i,0]}, {X[i,1]}) = {Y[i]}",
        (X[i, 0], X[i, 1]),
        xytext=(8, 8),
        textcoords="offset points"
    )

# Frontera de decision aprendida
if abs(pesos[1]) > 1e-10:

    xx = np.linspace(-0.3, 1.3, 100)
    yy = -(pesos[0] * xx + bias) / pesos[1]

    ax.plot(
        xx, yy,
        "b--",
        label="Frontera de decision"
    )

ax.set_xlim(-0.4, 1.5)
ax.set_ylim(-0.4, 1.5)
ax.set_xlabel("Entrada X1")
ax.set_ylabel("Entrada X2")
ax.set_title("Compuerta AND - Clasificacion del perceptron")
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

