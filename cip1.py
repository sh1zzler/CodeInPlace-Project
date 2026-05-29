'Use left and right arrow keys to move the paddle'
'Use R to restart after game over or win'
'This is my first Python project, hope you like it! (only consists of 1 level but I may add more later)'


import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Breakout Game")

# colours
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 200, 0)
COLORS = [(255,50,50),(255,165,0),(255,255,0),(50,200,50),(50,150,255),(180,50,255)]

# paddle and ball
paddle = pygame.Rect(250, 460, 100, 12)
ball   = pygame.Rect(295, 445, 12, 12)
bx, by = 4, -4

# make bricks
bricks = []
for row in range(6):
    for col in range(10):
        b = pygame.Rect(8 + col * 59, 50 + row * 28, 55, 22)
        bricks.append([b, COLORS[row]])

font = pygame.font.SysFont(None, 42)
clock = pygame.time.Clock()
clock.tick(60)
game_over = False
won = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # move paddle with arrow keys
    if keys[pygame.K_LEFT]  and paddle.left  > 0:    paddle.x -= 6
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH: paddle.x += 6

    if not game_over and not won:
        ball.x += bx
        ball.y += by

        # bounce off walls
        if ball.left <= 0 or ball.right >= WIDTH: bx *= -1
        if ball.top  <= 0:                        by *= -1

        # bounce off paddle
        if ball.colliderect(paddle) and by > 0:   by *= -1

        # ball fell off bottom
        if ball.top > HEIGHT:
            game_over = True

        # check brick collision
        for item in bricks:
            if ball.colliderect(item[0]):
                bricks.remove(item)
                by *= -1
                break

        if len(bricks) == 0:
            won = True

    # restart with R
    if keys[pygame.K_r] and (game_over or won):
        paddle = pygame.Rect(250, 460, 100, 12)
        ball   = pygame.Rect(295, 445, 12, 12)
        bx, by = 4, -4
        bricks = []
        for row in range(6):
            for col in range(10):
                b = pygame.Rect(8 + col * 59, 50 + row * 28, 55, 22)
                bricks.append([b, COLORS[row]])
        game_over = False
        won = False

    # draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.rect(screen, WHITE, ball)
    for item in bricks:
        pygame.draw.rect(screen, item[1], item[0])

    if game_over:
        screen.blit(font.render("Game Over! Press R to restart", True, WHITE), (100, 230))
    if won:
        screen.blit(font.render("Congratulations! You beat it!", True, GREEN), (95, 215))
        screen.blit(font.render("Press R to play again", True, WHITE), (170, 260))

    pygame.display.flip()
