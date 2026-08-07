import pygame

WIDTH = 16
HEIGHT = 8
SCALE = 25

def make_palette(): # grayscale
    palette_size = 128
    return [(i * 2, i * 2, i * 2) for i in range(palette_size)]

def run_color_viewer():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    palette = make_palette()

    font = pygame.font.SysFont(None, 14)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for i in range(128):
            x = (i % WIDTH) * SCALE
            y = (i // WIDTH) * SCALE

            pygame.draw.rect(screen, palette[i], (x, y, SCALE, SCALE))

            text = font.render(str(i), True, (255, 0, 0))
            screen.blit(text, (x + 2, y + 2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run_color_viewer()