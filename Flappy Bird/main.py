from random import randint
import pygame,math,sys,time
pygame.init()
WIDTH,HEIGHT = 1366,768
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def draw_screen():
    pass

def update():
    pass


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        update()
        draw_screen()
        pygame.display.flip()
        clock.tick(60)
