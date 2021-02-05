import sys
import pygame


def vitya_upal():
    pygame.quit()
    sys.exit()


def vitya_botayet():
    while 31791:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vitya_upal()
        pygame.display.flip()


def vitya_risuet():
    pass


if __name__ == '__main__':
    pygame.init()
    VITIN_SIZE = 500, 500
    vitin_screen = pygame.display.set_mode(VITIN_SIZE)
    pygame.display.set_caption('Витёк')

    vitya_botayet()
