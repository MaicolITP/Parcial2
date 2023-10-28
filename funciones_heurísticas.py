from random import shuffle  # Importa la función shuffle, pero no se usa en el código
from copy import deepcopy   # Importa la función deepcopy para realizar copias profundas
from colorama import Fore, Back, Style  # Importa módulos para colorear la salida en la consola

# Direcciones de movimiento
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

# Matriz objetivo
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Función para obtener la posición de un elemento en la matriz
def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

# Función para calcular el costo heurístico utilizando la distancia de Manhattan
def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

# Función para obtener nodos adyacentes al nodo actual
def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))

    return listNode

# Función para encontrar el mejor nodo en el conjunto de nodos abiertos
def getBestNode(openSet):
    bestNode = None
    bestF = None

    for node in openSet.values():
        if bestNode is None or node.f() < bestF:
            bestNode = node
            bestF = node.f()

    return bestNode

# Función para construir el camino desde el estado final hasta el estado inicial
def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

# Clase que representa un nodo en el grafo de búsqueda
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

# Función para imprimir el rompecabezas en la consola
def print_puzzle(matrix):
    for row in matrix:
        for num in row:
            if num == 0:
                print(Fore.RED + f"{num:2}" + Style.RESET_ALL, end=" ")
            else:
                print(f"{num:2}", end=" ")
        print()
    print()

# Función principal para resolver el rompecabezas
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

# Función para obtener la matriz inicial desde la entrada estándar
def get_matrix_from_input():
    matrix = []
    for i in range(3):
        row = []
        input_str = input(f"Ingresa los valores para la fila {i + 1} (separados por espacios): ")
        values = input_str.split()
        for j in range(3):
            try:
                value = int(values[j])
                if value < 0 or value > 8:
                    print("El valor debe estar entre 0 y 8.")
                    return None
                row.append(value)
            except ValueError:
                print("Por favor, ingresa números válidos.")
                return None
        matrix.append(row)
    return matrix

# Función principal para la interacción con el usuario en la consola
def main_console():
    print("Resolución del rompecabezas 8-puzzle")
    print("Ingresa los valores de la matriz:")
    matrix = None
    while matrix is None:
        matrix = get_matrix_from_input()

    solution = main(matrix)
    print("\nSolución:")
    for step in solution:
        if step['dir'] != '':
            direction = ''
            if step['dir'] == 'U':
                direction = 'ARRIBA'
            elif step['dir'] == 'R':
                direction = "DERECHA"
            elif step['dir'] == 'L':
                direction = 'IZQUIERDA'
            elif step['dir'] == 'D':
                direction = 'ABAJO'
            print(f'Mover {direction}:')
            print_puzzle(step['node'])

if __name__ == "__main__":
    main_console()

