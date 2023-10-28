import tkinter as tk
import random

class PuzzleGame:
    def __init__(self):
        # Inicialización de la ventana de la interfaz gráfica
        self.window = tk.Tk()
        self.window.title("Puzzle-8")
        self.window.configure(bg='#d3d3d3')  # Fondo gris claro
        
        # Creación de una lista que representa el tablero del juego
        self.board = list(range(1, 9)) + [None]
        random.shuffle(self.board)  # Mezcla aleatoriamente las fichas en el tablero
        
        # Creación de una lista de botones que representarán las fichas en la interfaz
        self.tiles = []
        for i in range(9):
            tile_text = str(self.board[i]) if self.board[i] is not None else ''
            tile = tk.Button(self.window, text=tile_text, width=5, height=2, command=lambda i=i: self.tile_click(i), font=('Arial', 16))
            tile.configure(bg='#87CEEB' if self.board[i] is not None else '#d3d3d3')  # Azul para las fichas, gris para el espacio vacío
            tile.grid(row=i//3, column=i%3, padx=0, pady=0)  # Coloca los botones en una cuadrícula 3x3
            self.tiles.append(tile)
        
        # Creación de botones para mostrar las heurísticas
        self.manhattan_btn = tk.Button(self.window, text="Manhattan Distance", command=self.show_manhattan_distance, bg='#90EE90', font=('Arial', 12))
        self.manhattan_btn.grid(row=3, column=0, sticky='nsew')
        
        self.out_of_place_btn = tk.Button(self.window, text="Out of Place", command=self.show_out_of_place, bg='#90EE90', font=('Arial', 12))
        self.out_of_place_btn.grid(row=3, column=1, sticky='nsew')
        
        # Creación de botón de reinicio
        self.restart_btn = tk.Button(self.window, text="Reiniciar", command=self.restart_game, bg='#90EE90', font=('Arial', 12))
        self.restart_btn.grid(row=3, column=2, sticky='nsew')
        
        # Configuración de los pesos de las columnas para que se expandan adecuadamente
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)

        # Actualización inicial de las heurísticas
        self.update_heuristics()
        
        # Inicio del bucle principal de la interfaz gráfica
        self.window.mainloop()

    def tile_click(self, i):
        index = self.board.index(None)
        if (i // 3 == index // 3 and abs(i - index) == 1) or (i % 3 == index % 3 and abs(i - index) == 3):
            self.swap(index, i)
            self.update_heuristics()
    
    def swap(self, i, j):
        self.board[i], self.board[j] = self.board[j], self.board[i]
        self.tiles[i].config(text=str(self.board[i]))
        self.tiles[j].config(text=str(self.board[j]))
    
    def manhattan_distance(self):
        distance = 0
        for i in range(1, 9):
            xi, yi = self.index(i)
            xj, yj = (i-1)//3, (i-1)%3
            distance += abs(xi-xj) + abs(yi-yj)
        return distance

    def out_of_place(self):
        return sum(i != j for i, j in zip(self.board, list(range(1, 9)) + [None]))

    def index(self, value):
        return self.board.index(value)//3, self.board.index(value)%3
    
    def update_heuristics(self):
        self.manhattan_btn.config(text="Distancia de Manhattan: {}".format(self.manhattan_distance()))
        self.out_of_place_btn.config(text="Fuera de lugar: {}".format(self.out_of_place()))
    
    def show_manhattan_distance(self):
        print("Manhattan Distance:", self.manhattan_distance())
    
    def show_out_of_place(self):
        print("Out of Place:", self.out_of_place())

    def restart_game(self):
        self.board = list(range(1, 9)) + [None]
        random.shuffle(self.board)
        for i in range(9):
            self.tiles[i].config(text=str(self.board[i]))
        self.update_heuristics()

if __name__ == "__main__":
    PuzzleGame()
