import pygame
import time
import random

WIDTH, HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Get pew-pew'd")

BG = pygame.transform.scale(
    pygame.image.load("Background.png"), (WIDTH, HEIGHT)
)

PLAYER_WIDTH = 200
PLAYER_HEIGHT = 200

PLAYER = pygame.image.load("gura.png")
PLAYER = pygame.transform.scale(PLAYER, (PLAYER_WIDTH, PLAYER_HEIGHT))


def draw():
    WIN.blit(BG, (0, 0))

    WIN.blit(
        PLAYER,
        (WIDTH // 2 - PLAYER_WIDTH // 2,
         HEIGHT - PLAYER_HEIGHT + 30)
    )

    pygame.display.update()


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw()

    pygame.quit()


if __name__ == "__main__":
    main()