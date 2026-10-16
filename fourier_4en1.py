
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# SERIES COMPLEJAS DE FOURIER
# CUATRO EJERCICIOS - GRAFICAS 2D Y 3D
# ============================================================


# ------------------------------------------------------------
# 1. FUNCIONES PERIODICAS
# ------------------------------------------------------------

def funcion_periodica(t, ejercicio):

    t = np.asarray(t, dtype=float)

    # EJERCICIO 1: TRES JOROBAS
    if ejercicio == 1:

        T = 4 * np.pi
        r = np.mod(t, T)

        return np.select(
            [
                (r >= 0) & (r < np.pi),
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

    # EJERCICIO 2: RECTA y = x
    elif ejercicio == 2:

        T = 4 * np.pi
        r = np.mod(t + np.pi, T) - np.pi

        return np.where(
            (r >= -np.pi) & (r < np.pi),
            r,
            0.0
        )

    # EJERCICIO 3: FUNCION DE OCHO PUNTOS
    elif ejercicio == 3:

        T = 16.0
        r = np.mod(t, T)

        return np.select(
            [
                (r >= 0) & (r < 1),
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
                6.0 - r,
                r - 8.0
            ],
            default=0.0
        )

    # EJERCICIO 4: SENAL RECTANGULAR
    elif ejercicio == 4:

        T = np.pi
        r = np.mod(t, T)

        # Modelo provisional: amplitud 2,
        # activa durante la mitad del periodo.
        return np.where(
            r < np.pi/2,
            2.0,
            0.0
        )

    else:
        raise ValueError("Ejercicio no valido.")


# ------------------------------------------------------------
# 2. DATOS DE CADA EJERCICIO
# ------------------------------------------------------------

def obtener_datos(ejercicio):

    nombres = {
        1: "Tres jorobas",
        2: "Recta y = x con intervalo en cero",
        3: "Funcion de ocho puntos",
        4: "Senal rectangular"
    }

    periodos = {
        1: 4*np.pi,
        2: 4*np.pi,
        3: 16.0,
        4: np.pi
    }

    T = periodos[ejercicio]
    L = T / 2
    w0 = 2*np.pi / T

    return nombres[ejercicio], T, L, w0


# ------------------------------------------------------------
# 3. CALCULO DE COEFICIENTES COMPLEJOS
# ------------------------------------------------------------

def calcular_coeficientes(ejercicio, N, M=6000):

    nombre, T, L, w0 = obtener_datos(ejercicio)

    # Metodo numerico de puntos medios
    dt = T / M

    t = (np.arange(M) + 0.5) * dt

    y = funcion_periodica(t, ejercicio)

    indices = np.arange(-N, N + 1)

    coeficientes = np.zeros(len(indices), dtype=complex)

    # Formula:
    # cn = (1/T) integral f(t)*exp(-i*n*w0*t) dt

    for j, n in enumerate(indices):

        exponencial = np.exp(-1j * n * w0 * t)

        integral = np.sum(y * exponencial) * dt

        coeficientes[j] = integral / T

    return indices, coeficientes


# ------------------------------------------------------------
# 4. RECONSTRUCCION DE FOURIER
# ------------------------------------------------------------

def reconstruir_fourier(x, indices, coeficientes, w0):

    resultado = np.zeros_like(x, dtype=complex)

    for n, cn in zip(indices, coeficientes):

        resultado += cn * np.exp(1j * n * w0 * x)

    return np.real(resultado)


# ------------------------------------------------------------
# 5. TRAYECTORIA COMPLEJA PARA LA GRAFICA 3D
# ------------------------------------------------------------

def trayectoria_compleja(x, indices, coeficientes, w0):

    # Se utiliza la representacion de frecuencias positivas:
    #
    # z(x) = c0 + 2*suma(cn*exp(i*n*w0*x)), n=1,...,N
    #
    # La parte real reconstruye la senal original.
    # La parte imaginaria muestra la trayectoria compleja.

    z = np.zeros_like(x, dtype=complex)

    for n, cn in zip(indices, coeficientes):

        if n == 0:

            z += cn

        elif n > 0:

            z += 2 * cn * np.exp(1j * n * w0 * x)

    return z


# ------------------------------------------------------------
# 6. MOSTRAR COEFICIENTES
# ------------------------------------------------------------

def mostrar_coeficientes(indices, coeficientes):

    print("\n" + "="*65)
    print("        COEFICIENTES COMPLEJOS DE FOURIER")
    print("="*65)

    print(
        f"{'n':>5} | "
        f"{'Parte real':>16} | "
        f"{'Parte imaginaria':>18}"
    )

    print("-"*65)

    for n, cn in zip(indices, coeficientes):

        print(
            f"{n:5d} | "
            f"{cn.real:16.8f} | "
            f"{cn.imag:18.8f}"
        )

    print("-"*65)

    posicion_cero = np.where(indices == 0)[0][0]

    print("\nCoeficiente constante:")
    print("c0 =", coeficientes[posicion_cero])


# ------------------------------------------------------------
# 7. GRAFICA 2D: ORIGINAL Y FOURIER
# ------------------------------------------------------------

def grafica_2d(x, original, reconstruccion, ejercicio, nombre, N):

    plt.figure(figsize=(12, 6))

    plt.plot(
        x,
        original,
        color="blue",
        linewidth=2,
        label="Funcion original"
    )

    plt.plot(
        x,
        reconstruccion,
        color="red",
        linestyle="--",
        linewidth=1.8,
        label=f"Fourier complejo (N={N})"
    )

    plt.axhline(0, color="black", linewidth=0.8)

    plt.title(
        f"Ejercicio {ejercicio}: {nombre}\n"
        f"Reconstruccion mediante Fourier complejo"
    )

    plt.xlabel("x")
    plt.ylabel("f(x)")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()


# ------------------------------------------------------------
# 8. GRAFICA 3D: TRAYECTORIA COMPLEJA
# ------------------------------------------------------------

def grafica_3d(x, z, ejercicio, nombre, N):

    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(
        111,
        projection="3d"
    )

    # Trayectoria compleja
    ax.plot(
        x,
        z.real,
        z.imag,
        linewidth=2,
        color="blue",
        label="Trayectoria compleja"
    )

    # Proyeccion de la parte real sobre Z=0
    ax.plot(
        x,
        z.real,
        np.zeros_like(x),
        linestyle="--",
        linewidth=1.5,
        color="red",
        label="Proyeccion real"
    )

    ax.set_xlabel("Tiempo (x)")
    ax.set_ylabel("Parte real")
    ax.set_zlabel("Parte imaginaria")

    ax.set_title(
        f"Fourier complejo en 3D\n"
        f"Ejercicio {ejercicio}: {nombre} - N={N}"
    )

    ax.legend()

    # Angulo inicial
    ax.view_init(
        elev=25,
        azim=-60
    )

    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 9. GRAFICAS DE COEFICIENTES
# ------------------------------------------------------------

def graficas_coeficientes(indices, coeficientes, ejercicio):

    # Magnitud de los coeficientes
    plt.figure(figsize=(11, 5))

    plt.stem(
        indices,
        np.abs(coeficientes)
    )

    plt.title(
        f"Magnitud de coeficientes complejos - Ejercicio {ejercicio}"
    )

    plt.xlabel("Indice n")
    plt.ylabel("|cn|")

    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Parte real e imaginaria
    plt.figure(figsize=(11, 5))

    plt.plot(
        indices,
        coeficientes.real,
        "o-",
        label="Parte real"
    )

    plt.plot(
        indices,
        coeficientes.imag,
        "s--",
        label="Parte imaginaria"
    )

    plt.axhline(0, color="black", linewidth=0.8)

    plt.title("Componentes de los coeficientes complejos")

    plt.xlabel("Indice n")
    plt.ylabel("Valor")

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# 10. PROCESAR EJERCICIO
# ------------------------------------------------------------

def procesar_ejercicio(ejercicio, N, tipo_grafica):

    nombre, T, L, w0 = obtener_datos(ejercicio)

    print("\nCalculando coeficientes...")

    indices, coeficientes = calcular_coeficientes(
        ejercicio,
        N
    )

    mostrar_coeficientes(indices, coeficientes)

    # Graficar tres periodos
    if ejercicio == 2:
        inicio = -np.pi - T
    else:
        inicio = -T

    x = np.linspace(
        inicio,
        inicio + 3*T,
        6000
    )

    original = funcion_periodica(x, ejercicio)

    reconstruccion = reconstruir_fourier(
        x,
        indices,
        coeficientes,
        w0
    )

    z = trayectoria_compleja(
        x,
        indices,
        coeficientes,
        w0
    )

    # Seleccionar graficas
    if tipo_grafica == 1:

        grafica_2d(
            x,
            original,
            reconstruccion,
            ejercicio,
            nombre,
            N
        )

    elif tipo_grafica == 2:

        grafica_3d(
            x,
            z,
            ejercicio,
            nombre,
            N
        )

    elif tipo_grafica == 3:

        grafica_2d(
            x,
            original,
            reconstruccion,
            ejercicio,
            nombre,
            N
        )

        grafica_3d(
            x,
            z,
            ejercicio,
            nombre,
            N
        )

        graficas_coeficientes(
            indices,
            coeficientes,
            ejercicio
        )


# ------------------------------------------------------------
# 11. MENU PRINCIPAL
# ------------------------------------------------------------

def menu():

    while True:

        print("\n")
        print("="*60)
        print("       SERIES COMPLEJAS DE FOURIER")
        print("          MENU PRINCIPAL 2D / 3D")
        print("="*60)

        print("1. Tres jorobas")
        print("2. Recta y = x")
        print("3. Funcion de ocho puntos")
        print("4. Senal rectangular")
        print("0. Salir")

        print("="*60)

        opcion = input(
            "\nSelecciona un ejercicio (0-4): "
        ).strip()

        if opcion == "0":

            print("\nPrograma finalizado.")
            break

        if opcion not in ["1", "2", "3", "4"]:

            print("\nOpcion incorrecta. Intenta nuevamente.")
            continue

        ejercicio = int(opcion)

        # Numero de armonicos
        entrada = input(
            "\nNumero de armonicos [10 por defecto]: "
        ).strip()

        if entrada == "":

            N = 10

        else:

            try:

                N = int(entrada)

                if N < 1 or N > 100:

                    print(
                        "\nIntroduce un valor entre 1 y 100."
                    )
                    continue

            except ValueError:

                print("\nDebes introducir un numero entero.")
                continue

        # Menu de graficas
        print("\n" + "="*60)
        print("              TIPO DE GRAFICA")
        print("="*60)

        print("1. Grafica 2D")
        print("2. Grafica 3D")
        print("3. Todas las graficas")

        print("="*60)

        entrada_grafica = input(
            "\nSelecciona una opcion (1-3): "
        ).strip()

        if entrada_grafica not in ["1", "2", "3"]:

            print("\nOpcion incorrecta.")
            continue

        tipo_grafica = int(entrada_grafica)

        nombre, T, L, w0 = obtener_datos(ejercicio)

        print("\n" + "="*60)
        print("EJERCICIO SELECCIONADO")
        print("="*60)

        print("Nombre:", nombre)
        print(f"Periodo T = {T:.8f}")
        print(f"L = {L:.8f}")
        print(f"Frecuencia fundamental = {w0:.8f}")
        print(f"Numero de armonicos = {N}")

        print("\nGenerando resultados...")

        procesar_ejercicio(
            ejercicio,
            N,
            tipo_grafica
        )

        input(
            "\nPresiona ENTER para regresar al menu..."
        )


# ------------------------------------------------------------
# 12. INICIO DEL PROGRAMA
# ------------------------------------------------------------

if __name__ == "__main__":

    menu()
