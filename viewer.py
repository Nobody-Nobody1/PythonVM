import pygame
import socket
import struct
import colorsys

def make_palette():
    palette = []
    for i in range(256):
        hue = i / 256
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        palette.append((int(r*255), int(g*255), int(b*255)))
    return palette

# --- Settings ---
WIDTH = 127
HEIGHT = 127
FPS = 60

# --- Setup Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Connect to frame stream ---
with socket.create_connection(("127.0.0.1", 9000)) as sock:
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Read frame size ---
        header = sock.recv(8)
        if not header:
            continue

        frame_size = struct.unpack("Q", header)[0]

        # --- Read frame data ---
        frame_data = b""
        while len(frame_data) < frame_size:
            chunk = sock.recv(frame_size - len(frame_data))
            if not chunk:
                break
            frame_data += chunk

        # --- Convert to Pygame surface ---
        frame_surface = pygame.image.frombuffer(frame_data, (WIDTH, HEIGHT), 'P')
        palette = make_palette()
        frame_surface.set_palette(palette)
        frame_surface.set_palette_at(0,(0,0,0))
        frame_surface.set_palette_at(1,(255,255,255))
        print(palette[0:11])

        # --- Draw frame ---
        screen.blit(frame_surface, (0, 0))

        # --- Update Screen ---
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()