# ============================================================
# EJERCICIO NxN
# ANÁLISIS TEMPORAL + OPTIMIZACIÓN DE POPULARIDAD
# ============================================================

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import time


# ============================================================
# CONFIGURACIÓN DE IMPRESIÓN
# ============================================================

np.set_printoptions(
    precision=4,
    suppress=True
)


# ============================================================
# 1. PEDIR TAMAÑO DE LA MATRIZ
# ============================================================

while True:

    try:

        n = int(
            input("\nIngresa el tamaño n de la matriz NxN: ")
        )

        if n >= 2:
            break

        print("El tamaño debe ser mínimo 2.")

    except ValueError:

        print("Debes ingresar un número entero.")


# ============================================================
# 2. CREAR NOMBRES DE LOS NODOS
# ============================================================

nodos = [
    f"N{i+1}"
    for i in range(n)
]


# ============================================================
# 3. GENERAR MATRIZ ALEATORIA DE CONEXIONES
# ============================================================
#
# A[origen, destino]
#
# 1 = existe conexión
# 0 = no existe conexión
#
# ============================================================

A = np.random.randint(
    0,
    2,
    size=(n, n)
)


# Eliminar conexiones consigo mismo

np.fill_diagonal(
    A,
    0
)


# ============================================================
# 4. GARANTIZAR AL MENOS UNA SALIDA POR NODO
# ============================================================

for i in range(n):

    if np.sum(A[i, :]) == 0:

        posibles = [
            j
            for j in range(n)
            if j != i
        ]

        destino = np.random.choice(
            posibles
        )

        A[i, destino] = 1


# ============================================================
# 5. FUNCIÓN PARA CREAR MATRIZ DE TRANSICIÓN
# ============================================================

def crear_matriz_transicion(A):

    tamaño = A.shape[0]

    M = np.zeros(
        (tamaño, tamaño),
        dtype=float
    )

    for origen in range(tamaño):

        destinos = np.where(
            A[origen, :] == 1
        )[0]

        cantidad = len(destinos)

        if cantidad > 0:

            peso = 1 / cantidad

            for destino in destinos:

                # destino = fila
                # origen = columna

                M[destino, origen] = peso

    return M


# ============================================================
# 6. FUNCIÓN PARA REALIZAR ANÁLISIS TEMPORAL
# ============================================================

def analizar(M, iteraciones):

    tamaño = M.shape[0]

    T = np.ones(
        (tamaño, 1),
        dtype=float
    ) / tamaño

    historial = [
        T.flatten().copy()
    ]

    for _ in range(iteraciones):

        T = M @ T

        historial.append(
            T.flatten().copy()
        )

    return T, np.array(historial)


# ============================================================
# 7. FUNCIÓN PARA COMPROBAR SI ES EL MÁS POPULAR
# ============================================================

def es_mas_popular(T, indice):

    popularidad_objetivo = T[indice, 0]

    for i in range(len(T)):

        if i != indice:

            if popularidad_objetivo <= T[i, 0]:

                return False

    return True


# ============================================================
# 8. FUNCIÓN PARA CALCULAR SEGUNDO MÁS POPULAR
# ============================================================

def segundo_mas_popular(T, indice_objetivo):

    valores = []

    for i in range(len(T)):

        if i != indice_objetivo:

            valores.append(
                T[i, 0]
            )

    return max(valores)


# ============================================================
# 9. FUNCIÓN PARA CALCULAR DISTORSIÓN
# ============================================================
#
# Mide cuánto cambió la distribución de popularidad.
#
# ============================================================

def calcular_distorsion(
    T_original,
    T_nueva
):

    return np.sum(
        np.abs(
            T_nueva[:, 0]
            -
            T_original[:, 0]
        )
    )


# ============================================================
# 10. IMPRIMIR MATRIZ ORIGINAL
# ============================================================

print("\n")
print("=" * 65)
print("             MATRIZ ORIGINAL DE CONEXIONES")
print("=" * 65)

print(A)


# ============================================================
# 11. IMPRIMIR CONEXIONES
# ============================================================

print("\n")
print("=" * 65)
print("                 CONEXIONES ORIGINALES")
print("=" * 65)


for i in range(n):

    for j in range(n):

        if A[i, j] == 1:

            print(
                f"{nodos[i]} ---> {nodos[j]}"
            )


# ============================================================
# 12. CREAR MATRIZ DE TRANSICIÓN
# ============================================================

M = crear_matriz_transicion(A)


print("\n")
print("=" * 65)
print("                  MATRIZ DE TRANSICIÓN M")
print("=" * 65)

print(M)


# ============================================================
# 13. COMPROBAR COLUMNAS
# ============================================================

print("\nSuma de las columnas:")

print(
    np.sum(
        M,
        axis=0
    )
)


# ============================================================
# 14. PEDIR NÚMERO DE ITERACIONES
# ============================================================

while True:

    try:

        iteraciones = int(
            input(
                "\n¿Cuántas iteraciones deseas realizar? "
            )
        )

        if iteraciones >= 1:
            break

        print(
            "El número de iteraciones debe ser mayor que cero."
        )

    except ValueError:

        print(
            "Debes ingresar un número entero."
        )


# ============================================================
# 15. ANÁLISIS TEMPORAL ORIGINAL
# ============================================================

inicio = time.perf_counter()


T_original, historial_original = analizar(
    M,
    iteraciones
)


fin = time.perf_counter()


tiempo_original = (
    fin - inicio
)


# ============================================================
# 16. IMPRIMIR TODAS LAS ITERACIONES
# ============================================================

print("\n")
print("=" * 65)
print("                 ANÁLISIS TEMPORAL")
print("=" * 65)


for k in range(
    iteraciones + 1
):

    print(
        f"\n---------------- T{k} ----------------"
    )

    for i in range(n):

        print(
            f"{nodos[i]} = "
            f"{historial_original[k, i] * 100:.4f}%"
        )


# ============================================================
# 17. MATRIZ M^k
# ============================================================

M_potencia = np.linalg.matrix_power(
    M,
    iteraciones
)


print("\n")
print("=" * 65)

print(
    f"                  NUEVA MATRIZ M^{iteraciones}"
)

print("=" * 65)

print(M_potencia)


# ============================================================
# 18. COMPROBACIÓN MATEMÁTICA
# ============================================================

T0 = np.ones(
    (n, 1)
) / n


T_comprobacion = (
    M_potencia @ T0
)


print("\n")
print("=" * 65)
print("                COMPROBACIÓN MATEMÁTICA")
print("=" * 65)


print(
    f"\nT{iteraciones} = "
    f"M^{iteraciones} x T0"
)


print("\nResultado:")

print(
    T_comprobacion
)


# ============================================================
# 19. RESULTADO ORIGINAL
# ============================================================

print("\n")
print("=" * 65)
print("              POPULARIDAD ANTES DEL CAMBIO")
print("=" * 65)


for i in range(n):

    print(
        f"{nodos[i]} = "
        f"{T_original[i,0] * 100:.4f}%"
    )


indice_original = np.argmax(
    T_original[:,0]
)


print(
    f"\nNodo más popular actualmente: "
    f"{nodos[indice_original]}"
)


print(
    f"Popularidad: "
    f"{T_original[indice_original,0] * 100:.4f}%"
)


print(
    f"\nTiempo de cálculo: "
    f"{tiempo_original:.9f} segundos"
)


# ============================================================
# 20. GRÁFICA TEMPORAL ORIGINAL
# ============================================================

plt.figure(
    figsize=(11,7)
)


for i in range(n):

    plt.plot(
        range(iteraciones + 1),
        historial_original[:,i] * 100,
        marker="o",
        label=nodos[i]
    )


plt.xlabel(
    "Iteración"
)

plt.ylabel(
    "Popularidad (%)"
)

plt.title(
    "Evolución temporal original"
)

plt.xticks(
    range(iteraciones + 1)
)

plt.legend(
    bbox_to_anchor=(1.05,1),
    loc="upper left"
)

plt.grid()

plt.tight_layout()

plt.show()


# ============================================================
# 21. CREAR GRAFO ORIGINAL
# ============================================================

G_original = nx.DiGraph()

G_original.add_nodes_from(
    nodos
)


for i in range(n):

    for j in range(n):

        if A[i,j] == 1:

            G_original.add_edge(
                nodos[i],
                nodos[j]
            )


# ============================================================
# 22. POSICIONES DE LOS NODOS
# ============================================================

pos = nx.spring_layout(
    G_original,
    seed=42
)


# ============================================================
# 23. GRAFICAR GRAFO ORIGINAL
# ============================================================

plt.figure(
    figsize=(11,8)
)


nx.draw_networkx_nodes(
    G_original,
    pos,
    node_size=2000
)


nx.draw_networkx_labels(
    G_original,
    pos,
    font_size=10,
    font_weight="bold"
)


nx.draw_networkx_edges(
    G_original,
    pos,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=25,
    width=1.8,
    connectionstyle="arc3,rad=0.08",
    min_source_margin=20,
    min_target_margin=20
)


plt.title(
    f"Grafo original {n} x {n}"
)


plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
# 24. PREGUNTAR QUÉ NODO HACER MÁS POPULAR
# ============================================================

print("\n")
print("=" * 65)
print("             SELECCIÓN DEL NODO OBJETIVO")
print("=" * 65)


print("\nNodos disponibles:\n")


for i in range(n):

    print(
        f"{i+1}. {nodos[i]} "
        f"({T_original[i,0] * 100:.4f}%)"
    )


while True:

    try:

        seleccion = int(
            input(
                f"\n¿Qué nodo deseas hacer el más popular? "
                f"(1-{n}): "
            )
        )

        if 1 <= seleccion <= n:

            break

        print(
            f"Selecciona un número entre 1 y {n}."
        )

    except ValueError:

        print(
            "Debes ingresar un número entero."
        )


indice_objetivo = (
    seleccion - 1
)


objetivo = nodos[
    indice_objetivo
]


print("\n")
print("=" * 65)
print("                  NODO SELECCIONADO")
print("=" * 65)


print(
    f"\nNodo objetivo: {objetivo}"
)


print(
    f"Popularidad actual: "
    f"{T_original[indice_objetivo,0] * 100:.4f}%"
)


# ============================================================
# 25. VERIFICAR SI YA ES EL MÁS POPULAR
# ============================================================

if es_mas_popular(
    T_original,
    indice_objetivo
):

    print("\n")
    print("=" * 65)

    print(
        f"{objetivo} YA ES EL NODO MÁS POPULAR"
    )

    print("=" * 65)

    print(
        "\nEnergía necesaria = 0"
    )

    print(
        "No es necesario modificar conexiones."
    )

    exit()


# ============================================================
# 26. GENERAR TODAS LAS CONEXIONES POSIBLES NUEVAS
# ============================================================
#
# Solamente agregaremos conexiones.
#
# No eliminamos conexiones originales.
#
# ============================================================

posibles_conexiones = []


for origen in range(n):

    for destino in range(n):

        if origen != destino:

            if A[
                origen,
                destino
            ] == 0:

                posibles_conexiones.append(
                    (
                        origen,
                        destino
                    )
                )


print("\n")
print("=" * 65)
print("           BÚSQUEDA DE MÍNIMA ENERGÍA")
print("=" * 65)


print(
    f"\nConexiones disponibles para agregar: "
    f"{len(posibles_conexiones)}"
)


# ============================================================
# 27. VARIABLES PARA GUARDAR LA MEJOR SOLUCIÓN
# ============================================================

mejor_combinacion = None

A_mejor = None

M_mejor = None

T_mejor = None

historial_mejor = None

energia_minima = None

mejor_margen = None

mejor_distorsion = None


# ============================================================
# 28. INICIAR TIMER DE OPTIMIZACIÓN
# ============================================================

inicio_optimizacion = time.perf_counter()


# ============================================================
# 29. BUSCAR MÍNIMA ENERGÍA
# ============================================================
#
# Energía = número de conexiones nuevas.
#
# Primero prueba:
#
# 1 conexión
#
# después:
#
# 2 conexiones
#
# después:
#
# 3 conexiones
#
# etc.
#
# Cuando encuentra soluciones en un nivel de energía,
# ya no prueba energías mayores.
#
# ============================================================

for energia in range(
    1,
    len(posibles_conexiones) + 1
):

    print(
        f"\nProbando energía = {energia}..."
    )


    soluciones_nivel = []


    for combinacion in itertools.combinations(
        posibles_conexiones,
        energia
    ):

        # ----------------------------------------------------
        # COPIAR MATRIZ ORIGINAL
        # ----------------------------------------------------

        A_prueba = A.copy()


        # ----------------------------------------------------
        # AGREGAR CONEXIONES
        # ----------------------------------------------------

        for origen, destino in combinacion:

            A_prueba[
                origen,
                destino
            ] = 1


        # ----------------------------------------------------
        # CREAR MATRIZ DE TRANSICIÓN MODIFICADA
        # ----------------------------------------------------

        M_prueba = crear_matriz_transicion(
            A_prueba
        )


        # ----------------------------------------------------
        # ANALIZAR LA RED
        # ----------------------------------------------------

        T_prueba, historial_prueba = analizar(
            M_prueba,
            iteraciones
        )


        # ----------------------------------------------------
        # VERIFICAR SI EL NODO OBJETIVO ES EL MÁS POPULAR
        # ----------------------------------------------------

        if es_mas_popular(
            T_prueba,
            indice_objetivo
        ):

            segundo = segundo_mas_popular(
                T_prueba,
                indice_objetivo
            )


            popularidad_objetivo = (
                T_prueba[
                    indice_objetivo,
                    0
                ]
            )


            # ------------------------------------------------
            # MARGEN SOBRE EL SEGUNDO LUGAR
            # ------------------------------------------------

            margen = (
                popularidad_objetivo
                -
                segundo
            )


            # ------------------------------------------------
            # DISTORSIÓN DE LA RED
            # ------------------------------------------------

            distorsion = calcular_distorsion(
                T_original,
                T_prueba
            )


            soluciones_nivel.append(
                (
                    margen,
                    distorsion,
                    combinacion,
                    A_prueba,
                    M_prueba,
                    T_prueba,
                    historial_prueba
                )
            )


    # ========================================================
    # SI ENCONTRAMOS SOLUCIONES
    # ========================================================

    if len(
        soluciones_nivel
    ) > 0:

        # ----------------------------------------------------
        # ORDEN:
        #
        # 1. Menor margen sobre segundo lugar.
        # 2. Menor distorsión de la red.
        #
        # La energía ya es mínima porque se prueba
        # progresivamente desde 1.
        # ----------------------------------------------------

        soluciones_nivel.sort(
            key=lambda x: (
                x[0],
                x[1]
            )
        )


        mejor = (
            soluciones_nivel[0]
        )


        mejor_margen = mejor[0]

        mejor_distorsion = mejor[1]

        mejor_combinacion = mejor[2]

        A_mejor = mejor[3]

        M_mejor = mejor[4]

        T_mejor = mejor[5]

        historial_mejor = mejor[6]

        energia_minima = energia


        break


# ============================================================
# 30. DETENER TIMER
# ============================================================

fin_optimizacion = time.perf_counter()


tiempo_optimizacion = (
    fin_optimizacion
    -
    inicio_optimizacion
)


# ============================================================
# 31. COMPROBAR SI EXISTE SOLUCIÓN
# ============================================================

if mejor_combinacion is None:

    print("\n")
    print("=" * 65)
    print("              NO SE ENCONTRÓ SOLUCIÓN")
    print("=" * 65)

    exit()


# ============================================================
# 32. MOSTRAR ENERGÍA MÍNIMA
# ============================================================

print("\n")
print("=" * 65)
print("                  SOLUCIÓN ÓPTIMA")
print("=" * 65)


print(
    f"\nNodo objetivo: "
    f"{objetivo}"
)


print(
    f"\nENERGÍA MÍNIMA = "
    f"{energia_minima}"
)


# ============================================================
# 33. MOSTRAR NUEVAS CONEXIONES
# ============================================================

print(
    "\nCONEXIONES NUEVAS:"
)


for origen, destino in mejor_combinacion:

    print(
        f"{nodos[origen]} "
        f"---> "
        f"{nodos[destino]}"
    )


# ============================================================
# 34. IMPRIMIR NUEVA MATRIZ DE CONEXIONES
# ============================================================

print("\n")
print("=" * 65)
print("          NUEVA MATRIZ DE CONEXIONES")
print("=" * 65)


print(
    A_mejor
)


# ============================================================
# 35. IMPRIMIR NUEVA MATRIZ DE TRANSICIÓN
# ============================================================

print("\n")
print("=" * 65)
print("        NUEVA MATRIZ DE TRANSICIÓN")
print("=" * 65)


print(
    M_mejor
)


# ============================================================
# 36. CALCULAR MATRIZ MODIFICADA ELEVADA A k
# ============================================================

M_mejor_potencia = np.linalg.matrix_power(
    M_mejor,
    iteraciones
)


print("\n")
print("=" * 65)

print(
    f"      MATRIZ MODIFICADA M^{iteraciones}"
)

print("=" * 65)


print(
    M_mejor_potencia
)


# ============================================================
# 37. MOSTRAR TODAS LAS ITERACIONES MODIFICADAS
# ============================================================

print("\n")
print("=" * 65)
print("           NUEVO ANÁLISIS TEMPORAL")
print("=" * 65)


for k in range(
    iteraciones + 1
):

    print(
        f"\n---------------- T{k} ----------------"
    )


    for i in range(n):

        print(
            f"{nodos[i]} = "
            f"{historial_mejor[k,i] * 100:.4f}%"
        )


# ============================================================
# 38. RESULTADO FINAL
# ============================================================

print("\n")
print("=" * 65)
print("                 RESULTADO FINAL")
print("=" * 65)


for i in range(n):

    print(
        f"{nodos[i]} = "
        f"{T_mejor[i,0] * 100:.4f}%"
    )


# ============================================================
# 39. ENCONTRAR SEGUNDO LUGAR
# ============================================================

otros = [
    i
    for i in range(n)
    if i != indice_objetivo
]


indice_segundo = max(
    otros,
    key=lambda i: T_mejor[i,0]
)


# ============================================================
# 40. COMPROBACIÓN FINAL
# ============================================================

print("\n")
print("=" * 65)
print("                COMPROBACIÓN FINAL")
print("=" * 65)


print(
    f"\nNodo elegido: "
    f"{objetivo}"
)


print(
    f"Popularidad original: "
    f"{T_original[indice_objetivo,0] * 100:.4f}%"
)


print(
    f"Popularidad final: "
    f"{T_mejor[indice_objetivo,0] * 100:.4f}%"
)


print(
    f"\nSegundo lugar: "
    f"{nodos[indice_segundo]}"
)


print(
    f"Popularidad segundo lugar: "
    f"{T_mejor[indice_segundo,0] * 100:.4f}%"
)


print(
    f"\nDiferencia sobre segundo lugar: "
    f"{mejor_margen * 100:.4f}%"
)


print(
    f"\nENERGÍA MÍNIMA = "
    f"{energia_minima}"
)


print(
    f"Distorsión de la red = "
    f"{mejor_distorsion * 100:.4f}%"
)


print(
    f"Tiempo de optimización = "
    f"{tiempo_optimizacion:.9f} segundos"
)


# ============================================================
# 41. GRAFO MODIFICADO
# ============================================================

G_nuevo = nx.DiGraph()

G_nuevo.add_nodes_from(
    nodos
)


# Agregar todas las conexiones nuevas

for i in range(n):

    for j in range(n):

        if A_mejor[i,j] == 1:

            G_nuevo.add_edge(
                nodos[i],
                nodos[j]
            )


# ============================================================
# 42. CONVERTIR NUEVAS CONEXIONES A NOMBRES
# ============================================================

nuevas_conexiones_grafica = []


for origen, destino in mejor_combinacion:

    nuevas_conexiones_grafica.append(
        (
            nodos[origen],
            nodos[destino]
        )
    )


# ============================================================
# 43. CONEXIONES ORIGINALES PARA LA GRÁFICA
# ============================================================

conexiones_originales_grafica = []


for i in range(n):

    for j in range(n):

        if A[i,j] == 1:

            conexiones_originales_grafica.append(
                (
                    nodos[i],
                    nodos[j]
                )
            )


# ============================================================
# 44. GRAFICAR RED MODIFICADA
# ============================================================

plt.figure(
    figsize=(12,8)
)


# NODOS

nx.draw_networkx_nodes(
    G_nuevo,
    pos,
    node_size=2200
)


# ETIQUETAS CON POPULARIDAD FINAL

etiquetas = {}


for i in range(n):

    etiquetas[nodos[i]] = (
        f"{nodos[i]}\n"
        f"{T_mejor[i,0] * 100:.2f}%"
    )


nx.draw_networkx_labels(
    G_nuevo,
    pos,
    labels=etiquetas,
    font_size=9,
    font_weight="bold"
)


# ============================================================
# CONEXIONES ORIGINALES
# ============================================================

nx.draw_networkx_edges(
    G_nuevo,
    pos,
    edgelist=conexiones_originales_grafica,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=25,
    width=1.8,
    edge_color="black",
    connectionstyle="arc3,rad=0.08",
    min_source_margin=20,
    min_target_margin=20
)


# ============================================================
# NUEVAS CONEXIONES EN ROJO
# ============================================================

nx.draw_networkx_edges(
    G_nuevo,
    pos,
    edgelist=nuevas_conexiones_grafica,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=30,
    width=4,
    edge_color="red",
    connectionstyle="arc3,rad=0.18",
    min_source_margin=20,
    min_target_margin=20
)


plt.title(
    f"Grafo optimizado\n"
    f"Nodo objetivo: {objetivo} | "
    f"Energía mínima = {energia_minima}"
)


plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
# 45. COMPARACIÓN DE POPULARIDADES
# ============================================================

x = np.arange(n)

ancho = 0.35


plt.figure(
    figsize=(11,7)
)


plt.bar(
    x - ancho/2,
    T_original[:,0] * 100,
    ancho,
    label="Antes"
)


plt.bar(
    x + ancho/2,
    T_mejor[:,0] * 100,
    ancho,
    label="Después"
)


plt.xlabel(
    "Nodos"
)


plt.ylabel(
    "Popularidad (%)"
)


plt.title(
    f"Popularidad antes y después\n"
    f"Nodo seleccionado: {objetivo}"
)


plt.xticks(
    x,
    nodos
)


plt.legend()

plt.grid(
    axis="y"
)

plt.tight_layout()

plt.show()


# ============================================================
# 46. EVOLUCIÓN DEL NODO OBJETIVO
# ============================================================

plt.figure(
    figsize=(10,6)
)


plt.plot(
    range(iteraciones + 1),
    historial_original[:,indice_objetivo] * 100,
    marker="o",
    label="Antes"
)


plt.plot(
    range(iteraciones + 1),
    historial_mejor[:,indice_objetivo] * 100,
    marker="o",
    label="Después"
)


plt.xlabel(
    "Iteración"
)


plt.ylabel(
    "Popularidad (%)"
)


plt.title(
    f"Evolución temporal del nodo {objetivo}"
)


plt.xticks(
    range(iteraciones + 1)
)


plt.legend()

plt.grid()

plt.tight_layout()

plt.show()


# ============================================================
# 48. RESUMEN FINAL
# ============================================================

print("\n")
print("=" * 65)
print("                    RESUMEN FINAL")
print("=" * 65)


print(
    f"\nMatriz: {n} x {n}"
)


print(
    f"Iteraciones: {iteraciones}"
)


print(
    f"Nodo seleccionado por el usuario: "
    f"{objetivo}"
)


print(
    f"Popularidad antes: "
    f"{T_original[indice_objetivo,0] * 100:.4f}%"
)


print(
    f"Popularidad después: "
    f"{T_mejor[indice_objetivo,0] * 100:.4f}%"
)


print(
    f"Segundo lugar: "
    f"{nodos[indice_segundo]} "
    f"({T_mejor[indice_segundo,0] * 100:.4f}%)"
)


print(
    f"Energía mínima utilizada: "
    f"{energia_minima}"
)


print(
    "\nNuevas conexiones:"
)


for origen, destino in mejor_combinacion:

    print(
        f"{nodos[origen]} ---> {nodos[destino]}"
    )


print("\n")
print("=" * 65)

print(
    f"{objetivo} ES AHORA EL NODO MÁS POPULAR"
)

print("=" * 65)

print("\nFIN DEL PROGRAMA")