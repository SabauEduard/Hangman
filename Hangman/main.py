import pygame
import math
import random
from pygame import mixer

# reset rectangle

RESET_SURFACE = pygame.display.set_mode((400, 300))

# display setup

pygame.init()
WIDTH, HEIGHT = 1000, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

# corner image

CORNER_IMAGE = pygame.image.load("thomas_shelby.jpg")

# button variables

RADIUS = 25
GAP = 20
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 550
letters = []
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(65 + i), True])

# load images

images = []
for index in range(7):
    images.append(pygame.image.load("hangman" + str(index) + ".png"))

# game variables

hangman_status = 0
words = ["SIGMA", "MINDSET", "ALPHA", "BILLIONAIRE", "SUCCESSFUL", "ENTREPRENEUR", "STARTUP", "ROUTINE",
         "DISCIPLINE", "MOTIVATION", "WOLF", "PACK", "LEADER", "GRIND", "WORK", "MORNING", "GRINDSET", "STOCKS",
         "CRYPTO", "BITCOIN", "WEALTH", "ASSET", "INCOME", "ETHEREUM", "TRADING"]
word = random.choice(words)
guessed = []

# fonts

LETTER_FONT = pygame.font.SysFont('comicsans', 35)
WORD_FONT = pygame.font.SysFont('comiscsans', 70)
TITLE_FONT = pygame.font.SysFont('comicsans', 80)

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# music

mixer.init()
BACKGROUND_MUSIC = pygame.mixer.Sound("sigma_male.wav")
BACKGROUND_MUSIC.set_volume(0.3)
BACKGROUND_MUSIC.play()

# game loop setup

FPS = 60
clock = pygame.time.Clock()
run = True


def draw():
    window.fill(WHITE)
    window.blit(CORNER_IMAGE, (70, 0))

    text = TITLE_FONT.render("HANGMAN", True, BLACK)
    pygame.draw.rect(window, BLACK, pygame.Rect(0.8 * WIDTH, 30, 150, 80), 5)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 5))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, True, BLACK)
    window.blit(text, (500, 400))

    for letter in letters:
        x, y, lttr, visible = letter
        if visible is True:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(lttr, True, BLACK)
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    window.blit(images[hangman_status], (100, 150))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    window.fill(WHITE)
    text = WORD_FONT.render(message, True, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, lttr, visible = letter
                if visible is True:
                    distance = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)
                    if distance < RADIUS:
                        letter[3] = False
                        guessed.append(lttr)
                        if lttr not in word:
                            hangman_status += 1

    draw()

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won is True:
        display_message("STRONG!")
        break

    if hangman_status == 6:
        display_message("WEAK!")
        break


pygame.quit()
