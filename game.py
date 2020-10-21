import pygame
import sys
import os
import random

pygame.init()

path = os.getcwd()

bg = pygame.transform.scale2x(pygame.image.load(f'{path}/Images/index.jpg'))

char = [
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R1.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R2.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R3.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R4.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R5.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R6.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R7.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R8.png'), 0, (14 / 18)),
    pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/R9.png'), 0, (14 / 18)),
]

charFlipped = [
    pygame.transform.flip(char[0], False, True),
    pygame.transform.flip(char[1], False, True),
    pygame.transform.flip(char[2], False, True),
    pygame.transform.flip(char[3], False, True),
    pygame.transform.flip(char[4], False, True),
    pygame.transform.flip(char[5], False, True),
    pygame.transform.flip(char[6], False, True),
    pygame.transform.flip(char[7], False, True),
    pygame.transform.flip(char[8], False, True),
]

fireball = [
    pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/FB001.png'), 0, 3), True, False),
    pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/FB002.png'), 0, 3), True, False),
    pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/FB003.png'), 0, 3), True, False),
    pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/FB004.png'), 0, 3), True, False),
    pygame.transform.flip(pygame.transform.rotozoom(pygame.image.load(f'{path}/Images/FB005.png'), 0, 3), True, False)
]

winLength = 400
winWidth = 336

screen = pygame.display.set_mode((winLength, winWidth))
pygame.display.set_caption("Space Adventures")

clock = pygame.time.Clock()

class Background(object):
    def __init__(self, speed):
        self.bgx1 = 0
        self.bgx2 = self.bgx1 + winLength
        self.speed = speed

    def draw(self):
        if self.bgx1 < (0 - winLength):
            self.bgx1 = winLength
        if self.bgx2 < (0 - winLength):
            self.bgx2 = self.bgx1 + winLength

        screen.blit(bg, (self.bgx1, 0))
        screen.blit(bg, (self.bgx2, 0))

    def move(self):
        self.bgx1 -= self.speed
        self.bgx2 -= self.speed


class Player(object):
    def __init__(self, x, vel, buffer):
        self.x = x
        self.y = 128
        self.vel = vel
        self.buffer = buffer
        self.count = 0
        self.flipped = False
        self.width = 64 * (14 / 18)

    def draw(self):
        if self.count + 1 >= 63:
            self.count = 0
        self.count += 1

        if self.flipped is False:
            screen.blit(char[self.count // 7], (self.x, self.y))
        if self.flipped is True:
            screen.blit(charFlipped[self.count // 7], (self.x, self.y))

    def move(self):
        if self.flipped is False and self.y < winWidth - self.buffer - self.width:
            self.y += self.vel
        if self.flipped is True and self.y > self.buffer:
            self.y -= self.vel

    def getMask(self):
        if self.flipped is False:
            return pygame.mask.from_surface(char[self.count // 7])
        else:
            return pygame.mask.from_surface((charFlipped[self.count // 7]))


class Fireball(object):
    def __init__(self, x):
        self.vel = 10
        self.x = x
        self.count = 0
        self.passed = False
        self.vel = 2
        self.gety()

    def gety(self):
        self.y = random.randrange(0, 300, 50)

    def draw(self):
        if self.count + 1 >= 35:
            self.count = 0
        self.count += 1

        screen.blit(fireball[self.count // 7], (self.x, self.y))

    def move(self):
        self.x -= self.vel

    def collide(self):
        self.charMask = character.getMask()
        self.fireballmask = pygame.mask.from_surface(fireball[self.count // 7])

        offset = (self.x - character.x, self.y - round(character.y))

        self.collisionPoint = self.charMask.overlap(self.fireballmask, offset)

        if self.collisionPoint:
            return True
        else:
            return False


background = Background(0.5)
character = Player(128, 2, 32)
meteors = [Fireball(300)]


def gameWindow(meteors):
    background.draw()
    character.draw()
    for ball in meteors:
        ball.draw()
    pygame.display.update()


def game():
    running = True

    score = 0

    while running:

        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                character.flipped = not character.flipped

        rem = []
        add_meteor = False
        for meteor in meteors:
            meteor.move()

            if meteor.collide():
                pygame.time.delay(1000)
                running = False

            if meteor.x < -100:
                rem.append(meteor)

            if not meteor.passed and meteor.x < character.x:
                meteor.passed = True
                add_meteor = True
                score += 1

        if add_meteor:
            meteors.append(Fireball(300))

        for r in rem:
            meteors.remove(r)

        background.move()
        character.move()
        gameWindow(meteors)

    pygame.display.quit()
    pygame.quit()
    return score
