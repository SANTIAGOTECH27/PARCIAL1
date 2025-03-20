import pygame
import sys
import random
from tkinter import messagebox, Tk

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
CELL_SIZE = 30
ROWS = 11
COLS = 21
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + 50

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Laberinto mejorado (1 = pared, 0 = camino, 2 = punto, 3 = inicio de fantasmas)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Inicializar pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Clase para el jugador
class Player:
    def __init__(self):
        self.x, self.y = 1, 1
        self.lives = 3
        self.score = 0
    
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < ROWS and 0 <= new_x < COLS and MAZE[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y
            if MAZE[self.y][self.x] == 2:
                self.score += 10
                MAZE[self.y][self.x] = 0

# Clase para los fantasmas
class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def move(self):
        if random.randint(0, 1) == 0:  # Reduce la frecuencia de movimiento
            directions = [(0,1), (1,0), (0,-1), (-1,0)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_y < ROWS and 0 <= new_x < COLS and MAZE[new_y][new_x] != 1:
                    self.x = new_x
                    self.y = new_y
                    break

# Inicializar jugador y fantasmas
player = Player()
ghosts = [Ghost(9, 4), Ghost(10, 4), Ghost(5, 4), Ghost(14, 4)]

game_over = False
# Bucle del juego
while not game_over:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            elif event.key == pygame.K_UP:
                player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
    
    # Dibujar laberinto
    for row in range(ROWS):
        for col in range(COLS):
            if MAZE[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif MAZE[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 5)
    
    # Dibujar jugador
    pygame.draw.circle(screen, YELLOW, (player.x * CELL_SIZE + CELL_SIZE // 2, player.y * CELL_SIZE + CELL_SIZE // 2), 10)
    
    # Mover y dibujar fantasmas
    for ghost in ghosts:
        ghost.move()
        pygame.draw.circle(screen, RED, (ghost.x * CELL_SIZE + CELL_SIZE // 2, ghost.y * CELL_SIZE + CELL_SIZE // 2), 10)
        if player.x == ghost.x and player.y == ghost.y:
            player.lives -= 1
            if player.lives == 0:
                root = Tk()
                root.withdraw()
                if messagebox.askyesno("Game Over", "¿Quieres jugar de nuevo?"):
                    player = Player()
                else:
                    game_over = True
                root.destroy()
    
    # Mostrar vidas
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Vidas: {player.lives}", True, WHITE)
    screen.blit(lives_text, (10, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(10)
