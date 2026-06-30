import threading

class ProgramState:
    def __init__(self, maze):
        """
        Inicializa el estado compartido leyendo los datos reales de la instancia MazeGen.
        """
        # --- Referencia al generador ---
        self.maze_data = maze  # Guardamos la referencia a vuestro objeto MazeGen
        
        # --- Configuración de Escala Gráfica ---
        self.block_size = 10  # Tamaño en píxeles de cada bloque/subcelda en la pantalla
        
        # --- Traducir vuestro diccionario a una matriz visual simple ---
        # La matriz tendrá dimensiones ampliadas para poder pintar los muros físicos.
        # Un valor 1 = Muro, 0 = Camino, 2 = Patrón '42'
        self.visual_matrix = self._translate_maze_to_matrix()
        
        # --- Traducir vuestra ruta de solución a coordenadas visuales ---
        self.visual_solution = self._translate_solution_to_matrix_coords()
        
        # --- Variables de Control de Interfaz (Menú y Animación) ---
        self.show_solution = False      # True = Muestra la solución de golpe (Opción 2)
        self.animate_solution = False   # True = Activa la animación paso a paso (Opción 5)
        self.current_step = 0           # Cuántos pasos de la solución se deben pintar actualmente
        
        # --- Configuración de Colores (Opción 3) ---
        self.current_palette = 0
        self.palettes = [
            # Formato: (Color Muro, Color Camino, Color Solución, Color 42)
            (0x2C3E50, 0xECF0F1, 0xE74C3C, 0x3498DB),  # Paleta 0: Elegante (Gris oscuro, Blanco, Rojo, Azul)
            (0x7A1E63, 0xFFEB3B, 0xFF5722, 0x00E5FF)   # Paleta 2: Psicodélico (Morado, Amarillo, Naranja, Cian)
        ]
        
        # --- Control del Hilo ---
        self.is_running = True          # Controla si el programa sigue vivo (Opción 4)

    def _translate_maze_to_matrix(self):
        """
        Transforma vuestro dict self.maze en una matriz de enteros de (width * 3) x (height * 3).
        Cada celda lógica se expande a un bloque de 3x3 para representar sus paredes internas.
        """
        w, h = self.maze_data.width, self.maze_data.height
        # Inicializamos todo el lienzo lleno de muros (1)
        matrix = [[1 for _ in range(w * 3)] for _ in range(h * 3)]
        
        for (x, y), cell in self.maze_data.maze.items():
            # Centro de la celda en la matriz visual
            cx, cy = x * 3 + 1, y * 3 + 1
            
            # El centro siempre es un camino (0), o un bloque '42' (2) si estaba congelado
            matrix[cy][cx] = 2 if cell.freeze else 0
            
            # Si la pared correspondiente está abierta (0 en vuestro dict), abrimos el camino en la matriz visual
            if cell.walls['north'] == 0: matrix[cy - 1][cx] = 0
            if cell.walls['south'] == 0: matrix[cy + 1][cx] = 0
            if cell.walls['east'] == 0:  matrix[cy][cx + 1] = 0
            if cell.walls['west'] == 0:  matrix[cy][cx - 1] = 0
            
        return matrix

    def _translate_solution_to_matrix_coords(self):
        """
        Transforma vuestra lista de tuplas [(x, y)] de la solución a los centros 3x3 de la matriz visual.
        """
        visual_path = []
        for (x, y) in self.maze_data.solution_path:
            cx, cy = x * 3 + 1, y * 3 + 1
            visual_path.append((cx, cy))
        return visual_path







#  Main:
# 2. CREACIÓN DEL PACTO INICIAL
    # Le pasamos todo vuestro generador a la clase del estado compartido
    state = ProgramState(maze)
    
    # A partir de aquí:
    # - El Miembro 1 leerá 'state.visual_matrix' para saber las filas y columnas exactas a pintar.
    # - El Miembro 2 leerá 'state.visual_solution' para controlar el recorrido del Bonus de animación.
    print(f"Matriz visual generada con éxito de tamaño: {len(state.visual_matrix[0])}x{len(state.visual_matrix)}")
