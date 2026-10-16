
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# SERIES COMPLEJAS DE FOURIER - CUATRO EJERCICIOS
# =====================================================

# CAMBIA ESTOS DOS VALORES PARA ELEGIR EL EJERCICIO
EJERCICIO = 1      # Opciones: 1, 2, 3 o 4
N = 10             # Numero de armonicos: 5, 10, 20, 40...
M = 4000           # Puntos para calcular las integrales

# -----------------------------------------------------
# FUNCIONES ORIGINALES EN UN PERIODO
# -----------------------------------------------------

def funcion_periodica(t, ejercicio):

    if ejercicio == 1:
        # Tres jorobas. Periodo T = 4*pi
        T = 4 * np.pi
        r = np.mod(t, T)

        return np.select(
            [
                r < np.pi,
                (r >= np.pi) & (r < 3*np.pi/2),
                (r >= 3*np.pi/2) & (r < 2*np.pi)
            ],
            [
                1 + np.sin(r),
                1 + np.sin(2*r),
                -np.sin(r)
            ],
            default=0.0
        )

    elif ejercicio == 2:
        # Recta y=x y despues un intervalo en cero
        # Periodo T = 4*pi
        T = 4 * np.pi
        r = np.mod(t + np.pi, T) - np.pi

        return np.where(
            (r >= -np.pi) & (r <= np.pi),
            r,
            0.0
        )

    elif ejercicio == 3:
        # Funcion lineal por tramos de 8 puntos
        # Activa de 0 a 8; cero de 8 a 16
        T = 16.0
        r = np.mod(t, T)

        return np.select(
            [
                r < 1,
                (r >= 1) & (r < 2),
                (r >= 2) & (r < 3),
                (r >= 3) & (r < 4),
                (r >= 4) & (r < 7),
                (r >= 7) & (r < 8)
            ],
            [
                r,
                1.0,
                r - 1,
                2.0,
                6 - r,
                r - 8
            ],
            default=0.0
        )

    elif ejercicio == 4:
        # Senal rectangular con periodo T = pi
        # Modelo provisional: amplitud 2 y ciclo activo 50 %
        T = np.pi
        r = np.mod(t, T)

        return np.where(r < np.pi/2, 2.0, 0.0)

    else:
        raise ValueError("El ejercicio debe ser 1, 2, 3 o 4.")


# -----------------------------------------------------
# DATOS DE CADA EJERCICIO
# -----------------------------------------------------

periodos = {
    1: 4*np.pi,
    2: 4*np.pi,
    3: 16.0,
    4: np.pi
}

nombres = {
    1: "Tres jorobas",
    2: "Recta y = x con intervalo en cero",
    3: "Funcion de los 8 puntos",
    4: "Senal rectangular"
}

T = periodos[EJERCICIO]
L = T / 2
w0 = 2*np.pi / T

# -----------------------------------------------------
# CALCULO NUMERICO DE COEFICIENTES COMPLEJOS
#
# cn = (1/T) integral f(t)*exp(-i*n*w0*t) dt
# -----------------------------------------------------

dt = T / M
t = (np.arange(M) + 0.5) * dt
y = funcion_periodica(t, EJERCICIO)

indices = np.arange(-N, N+1)

coeficientes = np.array([
    np.sum(y * np.exp(-1j*n*w0*t)) * dt / T
    for n in indices
])

# -----------------------------------------------------
# RECONSTRUCCION COMPLEJA DE FOURIER
# -----------------------------------------------------

x = np.linspace(-T, 2*T, 3000)

original = funcion_periodica(x, EJERCICIO)

fourier = np.zeros_like(x, dtype=complex)

for n, cn in zip(indices, coeficientes):
    fourier += cn * np.exp(1j*n*w0*x)

fourier = np.real(fourier)

# -----------------------------------------------------
# MOSTRAR RESULTADOS
# -----------------------------------------------------

print("=" * 55)
print("EJERCICIO:", EJERCICIO, "-", nombres[EJERCICIO])
print("=" * 55)

print(f"Periodo T = {T:.6f}")
print(f"L = {L:.6f}")
print(f"Frecuencia fundamental = {w0:.6f}")
print(f"Numero de armonicos = {N}")

print("\nCOEFICIENTES COMPLEJOS DE FOURIER")
print("-" * 55)
print(f"{'n':>5} {'Parte real':>15} {'Parte imaginaria':>18}")

for n, cn in zip(indices, coeficientes):
    print(f"{n:5d} {cn.real:15.7f} {cn.imag:18.7f}")

print("-" * 55)
print("c0 =", coeficientes[N])

# -----------------------------------------------------
# GRAFICAS
# -----------------------------------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    x, original,
    label="Funcion original",
    linewidth=2
)

plt.plot(
    x, fourier,
    "--",
    label=f"Serie compleja de Fourier (N={N})",
    linewidth=1.8
)

plt.title(f"Ejercicio {EJERCICIO}: {nombres[EJERCICIO]}")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------------------------------
# GRAFICA DE LOS COEFICIENTES
# -----------------------------------------------------

plt.figure(figsize=(11, 4))
plt.stem(indices, np.abs(coeficientes))
plt.title("Magnitud de los coeficientes complejos |cn|")
plt.xlabel("Indice n")
plt.ylabel("|cn|")
plt.grid(True)
plt.tight_layout()
plt.show()
