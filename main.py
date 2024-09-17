import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1300, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spidey Dodge")

# Load the background, player, and star images
bg = pygame.transform.scale(pygame.image.load("bg.png"), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load("ND.png"), (130, 100))  # Adjust the size to PLAYER_WIDTH and PLAYER_HEIGHT
star_img = pygame.transform.scale(pygame.image.load("bomb.png"), (50, 60))  # Adjust the size to STAR_WIDTH and STAR_HEIGHT

PLAYER_WIDTH = 130
PLAYER_HEIGHT = 100
STAR_WIDTH = 50
STAR_HEIGHT = 60

PLAYER_VEL = 5
STAR_VEL = 2

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(bg, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw the player image
    WIN.blit(player_img, (player.x, player.y))

    # Draw each star
    for star in stars:
        WIN.blit(star_img, (star.x, star.y))

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add new stars every few seconds
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        # Move stars and check for collision with the player
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "black")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()

# https://www.youtube.com/watch?v=waY3LfJhQLY