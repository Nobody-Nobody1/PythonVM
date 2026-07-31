import pygame
import socket
import struct

# --- Settings ---
WIDTH = 256
HEIGHT = 256
FPS = 60

# --- Setup Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Connect to frame stream ---
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 9000))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Read frame size ---
    header = sock.recv(4)
    if not header:
        continue

    frame_size = struct.unpack("I", header)[0]

    # --- Read frame data ---
    frame_data = b""
    while len(frame_data) < frame_size:
        chunk = sock.recv(frame_size - len(frame_data))
        if not chunk:
            break
        frame_data += chunk

    # --- Convert to Pygame surface ---
    frame_surface = pygame.image.frombuffer(frame_data, (WIDTH, HEIGHT), "RGB")

    # --- Draw frame ---
    screen.blit(frame_surface, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()