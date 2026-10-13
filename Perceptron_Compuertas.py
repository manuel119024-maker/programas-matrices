
import numpy as np
import matplotlib.pyplot as plt
import time

# ============================================================
# PERCEPTRON PARA COMPUERTAS LOGICAS
# AND - OR - NAND - NOR
# ENTRADA CONSTANTE X0 = 1
# ============================================================

np.random.seed(1)

# 1. MENU DE COMPUERTAS

compuertas = {
    1: ("AND",  [0, 0, 0, 1],
        "La salida es 1 solamente cuando ambas entradas son 1."),

    2: ("OR",   [0, 1, 1, 1],
        "La salida es 1 cuando al menos una entrada es 1."),

    3: ("NAND", [1, 1, 1, 0],
        "La salida es 0 solamente cuando ambas entradas son 1."),

    4: ("NOR",  [1, 0, 0, 0],
        "La salida es 1 solamente cuando ambas entradas son 0.")
}

print("\n==========================================")
print("    ENTRENAMIENTO DE COMPUERTAS LOGICAS")
print("==========================================")

for opcion, datos in compuertas.items():
    print(f"{opcion}. {datos[0]}")

while True:
    try:
        opcion = int(input("\nSelecciona una compuerta (1-4): "))

        if opcion in compuertas:
            break

        print("ERROR: Selecciona una opcion del 1 al 4.")

    except ValueError:
        print("ERROR: Ingresa un numero entero.")

nombre, salidas, descripcion = compuertas[opcion]

# 2. MATRIZ DE ENTRENAMIENTO
# X0 = 1 EN TODOS LOS PATRONES

X = np.array([
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
], dtype=float)

Y = np.array(salidas, dtype=int)

print("\n==========================================")
print(f"             COMPUERTA {nombre}")
print("==========================================")

print("\nFUNCIONAMIENTO:")
print(descripcion)

print("\nTABLA DE VERDAD:")
print(" X0  X1  X2  Salida deseada")

for i in range(len(X)):
    print(
        f" {int(X[i,0])}   {int(X[i,1])}   "
        f"{int(X[i,2])}         {Y[i]}"
    )

print("\nNOTA:")
print("X0 siempre vale 1.")
print("Su peso W0 incorpora el termino de sesgo.")
print("No existe una variable bias independiente.")

# 3. PARAMETROS DEL PERCEPTRON

pesos = np.random.uniform(-1, 1, 3)

alpha = 0.1
epocas = 100

historial_error = []
historial_precision = []

print("\n==========================================")
print("       CONFIGURACION DEL PERCEPTRON")
print("==========================================")

print("\nEntradas: X0, X1 y X2")
print("Numero de perceptrones: 1")
print("Funcion de activacion: Escalon")

print("\nPESOS INICIALES:")

for j in range(3):
    print(f"W{j} = {pesos[j]:.6f}")

print(f"\nTasa de aprendizaje = {alpha}")
print(f"Epocas maximas = {epocas}")

print("\nECUACION:")
print("z = W0*X0 + W1*X1 + W2*X2")

print("\nACTIVACION:")
print("Si z >= 0, salida = 1")
print("Si z <  0, salida = 0")

print("\nAPRENDIZAJE:")
print("error = deseada - obtenida")
print("W_nuevo = W_anterior + alpha*error*X")

# 4. FUNCION DE ACTIVACION

def activacion(z):
    return 1 if z >= 0 else 0


def predecir(entrada):
    z = np.dot(entrada, pesos)
    return activacion(z)


# 5. ENTRENAMIENTO

print("\n==========================================")
print("         INICIO DEL ENTRENAMIENTO")
print("==========================================")

inicio = time.perf_counter()

for epoca in range(1, epocas + 1):

    error_acumulado = 0

    print(f"\n--------------- EPOCA {epoca} ---------------")

    for i in range(len(X)):

        entrada = X[i]
        deseada = Y[i]

        pesos_anteriores = pesos.copy()

        # SUMA PONDERADA
        z = np.dot(entrada, pesos)

        # ACTIVACION
        obtenida = activacion(z)

        # ERROR
        error = deseada - obtenida

        error_acumulado += error**2

        print(f"\nPATRON {i+1}")

        print(
            f"Entradas: X0={int(entrada[0])}, "
            f"X1={int(entrada[1])}, "
            f"X2={int(entrada[2])}"
        )

        print("\n1. SUMA PONDERADA:")

        print(
            f"z = (1*{pesos[0]:.4f}) + "
            f"({int(entrada[1])}*{pesos[1]:.4f}) + "
            f"({int(entrada[2])}*{pesos[2]:.4f})"
        )

        print(f"z = {z:.6f}")

        print("\n2. ACTIVACION:")
        print(f"Salida deseada = {deseada}")
        print(f"Salida obtenida = {obtenida}")

        print("\n3. ERROR:")
        print(f"error = {deseada} - {obtenida} = {error}")

        # ACTUALIZACION DE LOS TRES PESOS
        pesos = pesos + alpha * error * entrada

        print("\n4. ACTUALIZACION DE PESOS:")

        if error == 0:
            print("Respuesta correcta. No hay ajuste.")
        else:
            print("Respuesta incorrecta. Se ajustan los pesos.")

        for j in range(3):

            ajuste = alpha * error * entrada[j]

            print(
                f"W{j}: {pesos_anteriores[j]:.4f} "
                f"+ ({ajuste:.4f}) = {pesos[j]:.4f}"
            )

    # ERROR CUADRATICO MEDIO DURANTE LA EPOCA

    mse = error_acumulado / len(X)
    historial_error.append(mse)

    # COMPROBACION CON LOS PESOS ACTUALIZADOS

    predicciones = np.array([
        predecir(entrada) for entrada in X
    ])

    precision = np.mean(predicciones == Y) * 100
    historial_precision.append(precision)

    print("\n==========================================")
    print(f"           RESUMEN EPOCA {epoca}")
    print("==========================================")

    print(f"Error de entrenamiento (MSE) = {mse:.6f}")
    print(f"Precision actual = {precision:.2f}%")

    print("\nPESOS ACTUALES:")

    for j in range(3):
        print(f"W{j} = {pesos[j]:.6f}")

    if precision == 100:
        print("\nAPRENDIZAJE COMPLETADO.")
        print("Los cuatro patrones son correctos.")
        break

fin = time.perf_counter()

# 6. RESULTADOS FINALES

print("\n==========================================")
print("             RESULTADOS FINALES")
print("==========================================")

print(f"\nCompuerta entrenada: {nombre}")

print("\n X0  X1  X2  Deseada  Obtenida  Estado")

predicciones_finales = []

for i in range(len(X)):

    obtenida = predecir(X[i])
    predicciones_finales.append(obtenida)

    estado = "CORRECTO" if obtenida == Y[i] else "ERROR"

    print(
        f" {int(X[i,0])}   {int(X[i,1])}   "
        f"{int(X[i,2])}      {Y[i]}        "
        f"{obtenida}     {estado}"
    )

predicciones_finales = np.array(predicciones_finales)

error_final = np.mean((Y - predicciones_finales)**2)
precision_final = np.mean(predicciones_finales == Y) * 100

print("\nPESOS APRENDIDOS:")

for j in range(3):
    print(f"W{j} = {pesos[j]:.6f}")

print("\nECUACION FINAL:")

print(
    f"z = ({pesos[0]:.4f}*1) + "
    f"({pesos[1]:.4f}*X1) + "
    f"({pesos[2]:.4f}*X2)"
)

print(f"\nError final = {error_final:.6f}")
print(f"Precision final = {precision_final:.2f}%")
print(f"Epocas realizadas = {len(historial_error)}")
print(f"Tiempo de entrenamiento = {fin-inicio:.6f} segundos")

# 7. GRAFICA DEL ERROR

plt.figure(figsize=(9, 5))

plt.plot(
    range(1, len(historial_error) + 1),
    historial_error,
    marker="o",
    linewidth=2,
    label="Error cuadratico medio"
)

plt.xlabel("Epocas")
plt.ylabel("Error cuadratico medio")
plt.title(f"Evolucion del error - {nombre}")
plt.grid(True)
plt.legend()
plt.tight_layout()

# 8. GRAFICA DE PRECISION

plt.figure(figsize=(9, 5))

plt.plot(
    range(1, len(historial_precision) + 1),
    historial_precision,
    marker="o",
    linewidth=2,
    label="Precision"
)

plt.xlabel("Epocas")
plt.ylabel("Precision (%)")
plt.title(f"Aprendizaje del perceptron - {nombre}")
plt.ylim(0, 105)
plt.grid(True)
plt.legend()
plt.tight_layout()

# 9. GRAFICA DE CLASIFICACION

fig, ax = plt.subplots(figsize=(8, 6))

for i in range(len(X)):

    x1 = X[i, 1]
    x2 = X[i, 2]

    color = "green" if Y[i] == 1 else "red"

    ax.scatter(x1, x2, color=color, s=180)

    ax.annotate(
        f"({int(x1)}, {int(x2)}) = {Y[i]}",
        (x1, x2),
        xytext=(8, 8),
        textcoords="offset points"
    )

# FRONTERA DE DECISION:
# W0 + W1*X1 + W2*X2 = 0

xx = np.linspace(-0.3, 1.3, 100)

if abs(pesos[2]) > 1e-10:

    yy = -(pesos[0] + pesos[1]*xx) / pesos[2]

    ax.plot(
        xx, yy,
        "b--",
        linewidth=2,
        label="Frontera de decision"
    )

elif abs(pesos[1]) > 1e-10:

    ax.axvline(
        -pesos[0] / pesos[1],
        color="blue",
        linestyle="--",
        linewidth=2,
        label="Frontera de decision"
    )

ax.set_xlim(-0.4, 1.5)
ax.set_ylim(-0.4, 1.5)
ax.set_xlabel("Entrada X1")
ax.set_ylabel("Entrada X2")
ax.set_title(f"Clasificacion de la compuerta {nombre}")
ax.grid(True)
ax.legend()
plt.tight_layout()

plt.show()

print("\nFIN DEL PROGRAMA")
