import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import time


# ============================================================
# GRAFO TEMPORAL
# HACER AL NODO ELEGIDO EL MÁS POPULAR
# CON LA MENOR ENERGÍA Y MENOR ALTERACIÓN DE LA RED
# ============================================================

nodos = ["A", "B", "C", "D", "E"]

N = len(nodos)


# ============================================================
# CONEXIONES ORIGINALES
# ============================================================

conexiones_originales = [

    ("A", "B"),
    ("A", "D"),

    ("B", "C"),
    ("B", "D"),

    ("C", "A"),
    ("C", "D"),
    ("C", "E"),

    ("D", "A"),
    ("D", "B"),

    ("E", "D")

]


# ============================================================
# CREAR MATRIZ DE TRANSICIÓN
# ============================================================

def crear_matriz(conexiones):

    M = np.zeros((N, N), dtype=float)

    for origen in nodos:

        destinos = [
            destino
            for o, destino in conexiones
            if o == origen
        ]

        numero_salidas = len(destinos)

        if numero_salidas > 0:

            peso = 1 / numero_salidas

            for destino in destinos:

                fila = nodos.index(destino)

                columna = nodos.index(origen)

                M[fila, columna] = peso

    return M


# ============================================================
# ANÁLISIS TEMPORAL
# ============================================================

def analizar(M, iteraciones):

    T = np.ones((N, 1)) / N

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
# VERIFICAR SI EL NODO ES EL MÁS POPULAR
# ============================================================

def es_mas_popular(T, indice):

    objetivo = T[indice, 0]

    for i in range(N):

        if i != indice:

            if objetivo <= T[i, 0]:

                return False

    return True


# ============================================================
# CALCULAR SEGUNDO MÁS POPULAR
# ============================================================

def segundo_mas_popular(T, indice_objetivo):

    valores = []

    for i in range(N):

        if i != indice_objetivo:

            valores.append(
                T[i, 0]
            )

    return max(valores)


# ============================================================
# DISTORSIÓN DE LA RED
# ============================================================
#
# Mide cuánto cambiaron las popularidades
# de TODOS los nodos respecto al resultado original.
#
# Menor valor = menor alteración.
#
# ============================================================

def calcular_distorsion(T_original, T_nueva):

    return np.sum(
        np.abs(
            T_nueva[:, 0]
            - T_original[:, 0]
        )
    )


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def mostrar(T):

    for i in range(N):

        print(
            f"{nodos[i]} = "
            f"{T[i,0]*100:.4f}%"
        )


# ============================================================
# MATRIZ ORIGINAL
# ============================================================

M_original = crear_matriz(
    conexiones_originales
)


print("\n============================================")
print("       MATRIZ DE TRANSICIÓN ORIGINAL")
print("============================================")

print(M_original)


# ============================================================
# NÚMERO DE ITERACIONES
# ============================================================

n = int(
    input(
        "\n¿Cuántas iteraciones deseas realizar? "
    )
)


if n <= 0:

    print(
        "El número de iteraciones debe ser mayor que cero."
    )

    exit()


# ============================================================
# ANÁLISIS ORIGINAL
# ============================================================

inicio = time.perf_counter()


T_original, historial_original = analizar(
    M_original,
    n
)


fin = time.perf_counter()


print("\n============================================")
print("         ANÁLISIS TEMPORAL ORIGINAL")
print("============================================")


for t in range(n + 1):

    print(
        f"\n------------- T{t} -------------"
    )

    for i in range(N):

        print(
            f"{nodos[i]} = "
            f"{historial_original[t,i]*100:.4f}%"
        )


print("\n============================================")
print("             RESULTADO ORIGINAL")
print("============================================")

mostrar(T_original)


indice_max = np.argmax(
    T_original[:,0]
)


print(
    f"\nNodo más popular originalmente: "
    f"{nodos[indice_max]}"
)


print(
    f"Popularidad máxima: "
    f"{T_original[indice_max,0]*100:.4f}%"
)


print(
    f"\nTiempo de cálculo: "
    f"{fin-inicio:.9f} segundos"
)


# ============================================================
# GRÁFICA TEMPORAL ORIGINAL
# ============================================================

plt.figure(figsize=(10,6))


for i in range(N):

    plt.plot(
        range(n + 1),
        historial_original[:,i]*100,
        marker="o",
        label=nodos[i]
    )


plt.xlabel("Iteración")

plt.ylabel("Popularidad (%)")

plt.title(
    "Evolución temporal original"
)

plt.xticks(
    range(n + 1)
)

plt.legend()

plt.grid()

plt.tight_layout()

plt.show()


# ============================================================
# POSICIONES DEL GRAFO
# ============================================================

pos = {

    "A": (0,2),

    "B": (3,2),

    "C": (3,0),

    "D": (0,0),

    "E": (5,0)

}


# ============================================================
# GRAFO ORIGINAL
# ============================================================

G_original = nx.DiGraph()

G_original.add_nodes_from(
    nodos
)

G_original.add_edges_from(
    conexiones_originales
)


plt.figure(figsize=(11,7))


nx.draw_networkx_nodes(
    G_original,
    pos,
    node_size=2200
)


nx.draw_networkx_labels(
    G_original,
    pos,
    font_size=16,
    font_weight="bold"
)


nx.draw_networkx_edges(
    G_original,
    pos,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=30,
    width=2,
    connectionstyle="arc3,rad=0.08",
    min_source_margin=20,
    min_target_margin=20
)


plt.title(
    "Grafo temporal original"
)

plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
# SELECCIONAR NODO
# ============================================================

print("\n============================================")
print("         OPTIMIZACIÓN DE POPULARIDAD")
print("============================================")


objetivo = input(
    "\n¿Qué nodo deseas hacer el más popular "
    "(A, B, C, D o E)? "
).upper()


if objetivo not in nodos:

    print(
        "\nNodo no válido."
    )

    exit()


indice_objetivo = nodos.index(
    objetivo
)


print(
    f"\nPopularidad actual de {objetivo}: "
    f"{T_original[indice_objetivo,0]*100:.4f}%"
)


# ============================================================
# COMPROBAR SI YA ES EL MÁS POPULAR
# ============================================================

if es_mas_popular(
    T_original,
    indice_objetivo
):

    print(
        f"\n{objetivo} ya es el nodo más popular."
    )

    print(
        "Energía necesaria = 0"
    )

    exit()


# ============================================================
# CREAR TODAS LAS CONEXIONES QUE PUEDEN AGREGARSE
# ============================================================
#
# IMPORTANTE:
#
# Ya NO vamos a eliminar conexiones existentes.
#
# Solamente agregamos ligas.
#
# De esta forma no dejamos sin popularidad
# a otros nodos.
#
# ============================================================

posibles = []


for origen in nodos:

    for destino in nodos:

        if origen != destino:

            conexion = (
                origen,
                destino
            )

            if conexion not in conexiones_originales:

                posibles.append(
                    conexion
                )


# ============================================================
# BÚSQUEDA DE MÍNIMA ENERGÍA
# ============================================================

print("\n============================================")
print("       BÚSQUEDA DE MÍNIMA ENERGÍA")
print("============================================")


inicio_busqueda = time.perf_counter()


solucion = None

T_solucion = None

M_solucion = None

historial_solucion = None

conexiones_solucion = None

margen_solucion = None

distorsion_solucion = None


# ============================================================
# PROBAR PRIMERO ENERGÍA 1
# DESPUÉS 2, 3...
# ============================================================

for energia in range(
    1,
    len(posibles) + 1
):

    print(
        f"\nProbando energía = {energia}..."
    )


    soluciones_nivel = []


    # ========================================================
    # COMBINACIONES CON ESA ENERGÍA
    # ========================================================

    for combinacion in itertools.combinations(
        posibles,
        energia
    ):

        conexiones_prueba = (
            conexiones_originales.copy()
        )


        # Agregar las ligas

        for conexion in combinacion:

            conexiones_prueba.append(
                conexion
            )


        # Crear nueva matriz

        M_prueba = crear_matriz(
            conexiones_prueba
        )


        # Realizar N iteraciones

        T_prueba, historial_prueba = analizar(
            M_prueba,
            n
        )


        # ====================================================
        # ¿EL NODO ELEGIDO ES EL MÁS POPULAR?
        # ====================================================

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


            # =================================================
            # MARGEN SOBRE EL SEGUNDO
            # =================================================
            #
            # Queremos que sea positivo,
            # pero LO MÁS PEQUEÑO POSIBLE.
            #
            # =================================================

            margen = (
                popularidad_objetivo
                - segundo
            )


            # =================================================
            # DISTORSIÓN TOTAL
            # =================================================

            distorsion = calcular_distorsion(
                T_original,
                T_prueba
            )


            soluciones_nivel.append(
                (
                    margen,
                    distorsion,
                    combinacion,
                    conexiones_prueba,
                    M_prueba,
                    T_prueba,
                    historial_prueba
                )
            )


    # ========================================================
    # SI EXISTEN SOLUCIONES CON ESTA ENERGÍA
    # ========================================================

    if len(soluciones_nivel) > 0:

        # ----------------------------------------------------
        # CRITERIO:
        #
        # 1. Ya estamos en la energía mínima.
        #
        # 2. Elegir el menor margen positivo sobre
        #    el segundo lugar.
        #
        # 3. Si hay empate, escoger la solución
        #    que menos altere la red.
        #
        # ----------------------------------------------------

        soluciones_nivel.sort(
            key=lambda x: (
                x[0],
                x[1]
            )
        )


        mejor = soluciones_nivel[0]


        margen_solucion = mejor[0]

        distorsion_solucion = mejor[1]

        solucion = mejor[2]

        conexiones_solucion = mejor[3]

        M_solucion = mejor[4]

        T_solucion = mejor[5]

        historial_solucion = mejor[6]


        energia_minima = energia


        break


fin_busqueda = time.perf_counter()


# ============================================================
# SI NO EXISTE SOLUCIÓN
# ============================================================

if solucion is None:

    print(
        "\nNo se encontró una solución."
    )

    exit()


# ============================================================
# RESULTADO DE LA OPTIMIZACIÓN
# ============================================================

print("\n============================================")
print("             SOLUCIÓN ÓPTIMA")
print("============================================")


print(
    f"\nENERGÍA MÍNIMA = "
    f"{energia_minima}"
)


print(
    "\nLIGAS AGREGADAS:"
)


for origen, destino in solucion:

    print(
        f"{origen} ---> {destino}"
    )


# ============================================================
# NUEVA MATRIZ
# ============================================================

print("\n============================================")
print("        NUEVA MATRIZ DE TRANSICIÓN")
print("============================================")

print(
    M_solucion
)


# ============================================================
# NUEVAS ITERACIONES
# ============================================================

print("\n============================================")
print("         NUEVO ANÁLISIS TEMPORAL")
print("============================================")


for t in range(n + 1):

    print(
        f"\n------------- T{t} -------------"
    )

    for i in range(N):

        print(
            f"{nodos[i]} = "
            f"{historial_solucion[t,i]*100:.4f}%"
        )


# ============================================================
# RESULTADO FINAL
# ============================================================

print("\n============================================")
print("               RESULTADO FINAL")
print("============================================")


mostrar(
    T_solucion
)


# ============================================================
# SEGUNDO MÁS POPULAR
# ============================================================

otros_indices = [

    i
    for i in range(N)
    if i != indice_objetivo

]


indice_segundo = max(
    otros_indices,
    key=lambda i: T_solucion[i,0]
)


print("\n============================================")
print("               COMPROBACIÓN")
print("============================================")


print(
    f"\nNodo elegido: "
    f"{objetivo}"
)


print(
    f"Popularidad final de {objetivo}: "
    f"{T_solucion[indice_objetivo,0]*100:.4f}%"
)


print(
    f"\nSegundo nodo más popular: "
    f"{nodos[indice_segundo]}"
)


print(
    f"Popularidad del segundo lugar: "
    f"{T_solucion[indice_segundo,0]*100:.4f}%"
)


print(
    f"\nDiferencia: "
    f"{margen_solucion*100:.4f}%"
)


print(
    f"\nENERGÍA MÍNIMA: "
    f"{energia_minima}"
)


print(
    f"Distorsión total de la red: "
    f"{distorsion_solucion*100:.4f}%"
)


print(
    f"\nTiempo de búsqueda: "
    f"{fin_busqueda-inicio_busqueda:.9f} segundos"
)


print("\n************************************")

print(
    f"{objetivo} ES EL NODO MÁS POPULAR"
)

print(
    "SIN REDUCIR INNECESARIAMENTE "
    "LA POPULARIDAD DE LOS DEMÁS"
)

print("************************************")


# ============================================================
# GRAFO MODIFICADO
# ============================================================

G_nuevo = nx.DiGraph()


G_nuevo.add_nodes_from(
    nodos
)


G_nuevo.add_edges_from(
    conexiones_solucion
)


plt.figure(figsize=(11,7))


# Nodos

nx.draw_networkx_nodes(
    G_nuevo,
    pos,
    node_size=2200
)


# Etiquetas

nx.draw_networkx_labels(
    G_nuevo,
    pos,
    font_size=16,
    font_weight="bold"
)


# ============================================================
# CONEXIONES ORIGINALES EN NEGRO
# ============================================================

nx.draw_networkx_edges(
    G_nuevo,
    pos,
    edgelist=conexiones_originales,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=30,
    width=2,
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
    edgelist=list(solucion),
    arrows=True,
    arrowstyle="-|>",
    arrowsize=35,
    width=4,
    edge_color="red",
    connectionstyle="arc3,rad=0.18",
    min_source_margin=20,
    min_target_margin=20
)


plt.title(
    f"Grafo optimizado\n"
    f"{objetivo} es el nodo más popular "
    f"con energía mínima = {energia_minima}"
)


plt.axis("off")

plt.tight_layout()

plt.show()


# ============================================================
# COMPARACIÓN ANTES Y DESPUÉS
# ============================================================

plt.figure(figsize=(10,6))


plt.plot(
    range(n + 1),
    historial_original[:,indice_objetivo]*100,
    marker="o",
    label="Antes"
)


plt.plot(
    range(n + 1),
    historial_solucion[:,indice_objetivo]*100,
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
    f"Popularidad del nodo {objetivo}\n"
    "Antes y después"
)


plt.xticks(
    range(n + 1)
)


plt.legend()

plt.grid()

plt.tight_layout()

plt.show()