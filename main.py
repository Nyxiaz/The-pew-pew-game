import pygame
import time
import random

pygame.init()
pygame.font.init()

# WINDOW
WIDTH, HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Salmon Rush!")

# BACKGROUND
BG = pygame.transform.scale(pygame.image.load("Background.png"),(WIDTH, HEIGHT))

# PLAYER
PLAYER_WIDTH = 200
PLAYER_HEIGHT = 200

PLAYER = pygame.image.load("gurap.png")
PLAYER = pygame.transform.scale(PLAYER,(PLAYER_WIDTH, PLAYER_HEIGHT))

PLAYER_X = WIDTH // 2 - PLAYER_WIDTH // 2
PLAYER_Y = HEIGHT - PLAYER_HEIGHT + 50

PLAYER_VEL = 5

# STARS
STAR_WIDTH = 60
STAR_HEIGHT = 60
STAR_VEL = 5

STAR = pygame.image.load("star.png")
STAR = pygame.transform.scale(STAR,(STAR_WIDTH, STAR_HEIGHT))

# SALMON
SALMON_WIDTH = 60
SALMON_HEIGHT = 60
SALMON_VEL = 5

SALMON = pygame.image.load("salmon.png")
SALMON = pygame.transform.scale(SALMON,(SALMON_WIDTH, SALMON_HEIGHT))

#COLLISION
PLAYER_MASK = pygame.mask.from_surface(PLAYER)
STAR_MASK = pygame.mask.from_surface(STAR)
SALMON_MASK = pygame.mask.from_surface(SALMON)

# FONT
TIMER_FONT = pygame.font.SysFont("roboto", 30)
LOSE_FONT = pygame.font.SysFont("roboto", 80)


#DRAW FUNCTION
def draw(player_x, player_y, elapsed_time, stars, salmons, salmon_count):
    WIN.blit(BG, (0, 0))

    time_text = TIMER_FONT.render(f"Time: {round(elapsed_time)}s",True,(255, 255, 255))
    WIN.blit(time_text, (10, 10))

    salmon_text = TIMER_FONT.render(f"Salmon: {salmon_count}",True,(255,255,255))
    WIN.blit(salmon_text, (10, 45))

    for star_x, star_y in stars:
        WIN.blit(STAR, (star_x, star_y))

    for salmon_x, salmon_y in salmons:
        WIN.blit(SALMON, (salmon_x, salmon_y))

    WIN.blit(PLAYER, (player_x, player_y))

    pygame.display.update()

#game over screen function
def game_over_screen(elapsed_time, salmon_count):

    play_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 120, 50)
    quit_rect = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 50, 120, 50)

    play_scale = 0
    quit_scale = 0
    clock = pygame.time.Clock()

    while True:

        WIN.blit(BG, (0, 0))

        lost_text = LOSE_FONT.render("You Lost!", True, "white")
        WIN.blit(lost_text,(WIDTH // 2 - lost_text.get_width() // 2,HEIGHT // 2 - 100))

        time_text = TIMER_FONT.render(f"Time: {elapsed_time}s",True,"white")
        WIN.blit(time_text,(WIDTH // 2 - time_text.get_width() // 2,HEIGHT // 2 - 20))

        salmon_text = TIMER_FONT.render(f"Salmon: {salmon_count}", True, "white")
        WIN.blit(salmon_text,(WIDTH // 2 - salmon_text.get_width() // 2,HEIGHT // 2 + 15))

        mouse_pos = pygame.mouse.get_pos()

        play_hover = play_rect.collidepoint(mouse_pos)
        quit_hover = quit_rect.collidepoint(mouse_pos)

        if play_hover:
            play_scale = min(play_scale + 1, 12)
        else:
            play_scale = max(play_scale - 1, 0)

        if quit_hover:
            quit_scale = min(quit_scale + 1, 12)
        else:
            quit_scale = max(quit_scale - 1, 0)

        play_draw_rect = play_rect.inflate(play_scale, play_scale)
        quit_draw_rect = quit_rect.inflate(quit_scale, quit_scale)

        pygame.draw.rect(WIN,"white",play_draw_rect,2,border_radius=10)

        pygame.draw.rect(WIN,"white",quit_draw_rect,2,border_radius=10)

        play_text = TIMER_FONT.render("PLAY", True, "white")
        quit_text = TIMER_FONT.render("QUIT", True, "white")

        WIN.blit(play_text,(play_draw_rect.centerx - play_text.get_width() // 2,play_draw_rect.centery - play_text.get_height() // 2 ))

        WIN.blit(quit_text,(    quit_draw_rect.centerx - quit_text.get_width() // 2,    quit_draw_rect.centery - quit_text.get_height() // 2))

        pygame.display.update()

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_rect.collidepoint(event.pos):
                    return True

                if quit_rect.collidepoint(event.pos):
                    return False


#MAIN FUNCTION
def main():
    global PLAYER_X, PLAYER_Y

    run = True
    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 1500
    star_count = 0
    stars = []

    hit = False

    salmon_count = 0
    salmons = []
    salmon_spawn_chance = 20

    while run:

        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # SPAWN STARS
        if star_count >= star_add_increment:

            for _ in range(3):

                valid_position = False

                while not valid_position:
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star_y = random.randint(-300, -STAR_HEIGHT)

                    valid_position = True

                    for existing_star in stars:
                        if abs(star_x - existing_star[0]) < STAR_WIDTH:
                            valid_position = False
                            break

                stars.append([star_x, star_y])

            #Salmon spawn
            if random.randint(1, 100) <= salmon_spawn_chance:
                valid_salmon_position = False
                while not valid_salmon_position:
                    salmon_x = random.randint(0,WIDTH - SALMON_WIDTH)
                    valid_salmon_position = True
                    for star in stars:
                        if abs(salmon_x - star[0]) < STAR_WIDTH + 20:
                            valid_salmon_position = False
                            break
                salmon_y = -SALMON_HEIGHT
                salmons.append([salmon_x, salmon_y])


            star_add_increment = max(100,star_add_increment - 10)

            star_count = 0

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and PLAYER_X > 0:
            PLAYER_X -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and PLAYER_X < WIDTH - PLAYER_WIDTH:
            PLAYER_X += PLAYER_VEL

        # SALMON MOVEMENT + COLLISION
        for salmon in salmons[:]:

            salmon[1] += SALMON_VEL
            offset = (salmon[0] - PLAYER_X, salmon[1] - PLAYER_Y)

            if PLAYER_MASK.overlap(SALMON_MASK, offset):
                salmons.remove(salmon)
                salmon_count += 1
                continue

            if salmon[1] > HEIGHT:
                salmons.remove(salmon)

        # STAR MOVEMENT + COLLISION
        for star in stars[:]:
            star[1] += STAR_VEL

            if star[1] > HEIGHT:
                stars.remove(star)
                continue

            offset = (star[0] - PLAYER_X, star[1] - PLAYER_Y)

            if PLAYER_MASK.overlap(STAR_MASK, offset):
                stars.remove(star)
                hit = True
                break

        # GAME OVER
        if hit:
            return game_over_screen(round(elapsed_time),salmon_count)



        draw(PLAYER_X,PLAYER_Y,elapsed_time,stars, salmons, salmon_count)

    pygame.quit()


if __name__ == "__main__":
    while True:

        restart = main()

        if not restart:
            break

    pygame.quit()