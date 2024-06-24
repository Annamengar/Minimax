# Importar las bibliotecas necesarias
import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración del tablero y los colores
TAMAÑO_CELDA = 100
TAMAÑO_TABLERO = 6
TAMAÑO_PANTALLA = TAMAÑO_CELDA * TAMAÑO_TABLERO
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((TAMAÑO_PANTALLA, TAMAÑO_PANTALLA))
pygame.display.set_caption('Gato y Ratón')

# Cargar imágenes
imagen_ratón = pygame.image.load('mouse.jpg')
imagen_gato = pygame.image.load('cat.jpg')
imagen_salida = pygame.image.load('escape.jpg')

# Escalar imágenes al tamaño de las celdas
imagen_ratón = pygame.transform.scale(imagen_ratón, (TAMAÑO_CELDA, TAMAÑO_CELDA))
imagen_gato = pygame.transform.scale(imagen_gato, (TAMAÑO_CELDA, TAMAÑO_CELDA))
imagen_salida = pygame.transform.scale(imagen_salida, (TAMAÑO_CELDA, TAMAÑO_CELDA))

# Clase Tablero para el tablero
class Tablero:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tablero = [['.' for _ in range(tamaño)] for _ in range(tamaño)]
        self.pos_ratón = (tamaño - 1, tamaño - 1)
        self.pos_gato = (0, 0)
        self.pos_salida = (random.randint(0, tamaño - 1), random.randint(0, tamaño - 1))
        while self.pos_salida == self.pos_ratón or self.pos_salida == self.pos_gato:
            self.pos_salida = (random.randint(0, tamaño - 1), random.randint(0, tamaño - 1))
        self.actualizar_tablero()
        self.posiciones_anteriores = {'R': self.pos_ratón, 'G': self.pos_gato}

    def actualizar_tablero(self):
        self.tablero = [['.' for _ in range(self.tamaño)] for _ in range(self.tamaño)]
        self.tablero[self.pos_ratón[0]][self.pos_ratón[1]] = 'R'
        self.tablero[self.pos_gato[0]][self.pos_gato[1]] = 'G'
        self.tablero[self.pos_salida[0]][self.pos_salida[1]] = 'S'

    def imprimir_tablero(self):
        for fila in self.tablero:
            print('|'.join(fila))
        print()

    def mover_pieza(self, pieza, nueva_pos):
        if pieza == 'R':
            self.posiciones_anteriores['R'] = self.pos_ratón
            self.pos_ratón = nueva_pos
        elif pieza == 'G':
            self.posiciones_anteriores['G'] = self.pos_gato
            self.pos_gato = nueva_pos
        self.actualizar_tablero()

    def obtener_movimientos_posibles(self, pos):
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        movimientos_posibles = []
        for d in direcciones:
            nueva_pos = (pos[0] + d[0], pos[1] + d[1])
            if 0 <= nueva_pos[0] < self.tamaño and 0 <= nueva_pos[1] < self.tamaño:
                movimientos_posibles.append(nueva_pos)
        return movimientos_posibles

    def es_juego_terminado(self, contador_turnos):
        if self.pos_gato == self.pos_ratón:
            return 'Gato Gana'
        elif self.pos_ratón == self.pos_salida:
            return 'Ratón Gana'
        elif contador_turnos >= 15:
            return 'Empate'
        return None

def evaluar(tablero):
    return abs(tablero.pos_ratón[0] - tablero.pos_gato[0]) + abs(tablero.pos_ratón[1] - tablero.pos_gato[1])

def minimax(tablero, profundidad, es_turno_ratón, alpha, beta):
    estado_juego = tablero.es_juego_terminado(contador_turnos)
    if profundidad == 0 or estado_juego:
        if estado_juego == 'Gato Gana':
            return -1000, None
        elif estado_juego == 'Ratón Gana':
            return 1000, None
        elif estado_juego == 'Empate':
            return 0, None
        return evaluar(tablero), None

    if es_turno_ratón:
        max_eval = float('-inf')
        mejor_movimiento = None
        for mov in tablero.obtener_movimientos_posibles(tablero.pos_ratón):
            tablero.mover_pieza('R', mov)
            eval, _ = minimax(tablero, profundidad - 1, False, alpha, beta)
            tablero.mover_pieza('R', tablero.posiciones_anteriores['R'])
            if eval > max_eval:
                max_eval = eval
                mejor_movimiento = mov
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, mejor_movimiento
    else:
        min_eval = float('inf')
        mejor_movimiento = None
        for mov in tablero.obtener_movimientos_posibles(tablero.pos_gato):
            tablero.mover_pieza('G', mov)
            eval, _ = minimax(tablero, profundidad - 1, True, alpha, beta)
            tablero.mover_pieza('G', tablero.posiciones_anteriores['G'])
            if eval < min_eval:
                min_eval = eval
                mejor_movimiento = mov
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, mejor_movimiento

def dibujar_rejilla():
    for x in range(0, TAMAÑO_PANTALLA, TAMAÑO_CELDA):
        pygame.draw.line(pantalla, NEGRO, (x, 0), (x, TAMAÑO_PANTALLA))
    for y in range(0, TAMAÑO_PANTALLA, TAMAÑO_CELDA):
        pygame.draw.line(pantalla, NEGRO, (0, y), (TAMAÑO_PANTALLA, y))

def dibujar_tablero(tablero):
    for fila in range(tablero.tamaño):
        for col in range(tablero.tamaño):
            rect = pygame.Rect(col * TAMAÑO_CELDA, fila * TAMAÑO_CELDA, TAMAÑO_CELDA, TAMAÑO_CELDA)
            pygame.draw.rect(pantalla, BLANCO, rect)
            pygame.draw.rect(pantalla, NEGRO, rect, 1)

            if (fila, col) == tablero.pos_ratón:
                pantalla.blit(imagen_ratón, rect.topleft)
            elif (fila, col) == tablero.pos_gato:
                pantalla.blit(imagen_gato, rect.topleft)
            elif (fila, col) == tablero.pos_salida:
                pantalla.blit(imagen_salida, rect.topleft)

def jugar():
    global contador_turnos
    tablero = Tablero(TAMAÑO_TABLERO)
    profundidad = 5
    contador_turnos = 0
    turno = 'R'

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill(BLANCO)
        dibujar_rejilla()
        dibujar_tablero(tablero)
        pygame.display.flip()

        estado_juego = tablero.es_juego_terminado(contador_turnos)
        if estado_juego:
            print(estado_juego)
            break

        if turno == 'R':
            _, movimiento = minimax(tablero, profundidad, True, float('-inf'), float('inf'))
            tablero.mover_pieza('R', movimiento)
            turno = 'G'
        else:
            _, movimiento = minimax(tablero, profundidad, False, float('-inf'), float('inf'))
            tablero.mover_pieza('G', movimiento)
            turno = 'R'

        # Imprimir las posiciones del ratón y el gato
        print(f"Turno {contador_turnos + 1}:")
        print(f"Posición del ratón: {tablero.pos_ratón}")
        print(f"Posición del gato: {tablero.pos_gato}")

        contador_turnos += 1
        pygame.time.delay(500)

    pantalla.fill(BLANCO)
    dibujar_rejilla()
    dibujar_tablero(tablero)
    pygame.display.flip()
    print("¡El juego ha terminado!")

# Iniciar el juego
jugar()
