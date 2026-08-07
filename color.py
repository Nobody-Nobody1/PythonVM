import pygame

WIDTH = 16
HEIGHT = 8
SCALE = 25
palette_size = 128

def make_palette(palette_size): # grayscale
    return [(i * 2, i * 2, i * 2) for i in range(palette_size)]

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
palette = make_palette(palette_size)

font = pygame.font.SysFont(None, 14)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(palette_size):
        x = (i % WIDTH) * SCALE
        y = (i // WIDTH) * SCALE

        pygame.draw.rect(screen, palette[i], (x, y, SCALE, SCALE))

        text = font.render(str(i), True, (255, 0, 0))
        screen.blit(text, (x + 2, y + 2))

    pygame.display.flip()

pygame.quit()