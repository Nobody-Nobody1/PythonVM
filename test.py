import pygame
import socket
import struct

# --- Settings ---
WIDTH = 127
HEIGHT = 127
FPS = 60

# --- Setup Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Draw frame ---
    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()