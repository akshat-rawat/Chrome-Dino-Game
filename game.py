import pygame
import os

pygame.font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 550
FLOOR = 430
STAT_FONT = pygame.font.SysFont("arial", 50)
END_FONT = pygame.font.SysFont("arial", 70)

score = 0
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

cactus_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "cactus1.png")).convert_alpha())
dino_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "dino" + str(x) + ".png"))) for x in
               range(1, 3)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")).convert_alpha())
jump_img = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "dinoJump.png")).convert_alpha())


class Dino:
    IMGS = dino_images
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 0
        self.isJump = False
        self.jumpCount = 0
        self.img_count = 0
        self.runCount = 0
        self.img = self.IMGS[0]
        self.hitbox = pygame.Rect(self.x + 4, self.y, self.width + 20, self.height + 30)

    def draw(self, win):
        if self.isJump:
            self.y -= self.jumpList[self.jumpCount] * 1.3
            win.blit(jump_img, (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.isJump = False
                self.runCount = 0
        else:
            if self.runCount >= 40:
                self.runCount = 0
            win.blit(self.IMGS[int(self.runCount//20)], (self.x, self.y))
            self.runCount += 1 + self.vel

        self.hitbox = pygame.Rect(self.x + 20, self.y, self.width + 5, self.height + 30)


class Cactus:
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.y = 350
        self.height = 64
        self.width = 64
        self.img = cactus_img
        self.passed = False
        self.hitbox = pygame.Rect(self.x, self.y, self.width - 20, self.height + 20)

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x, self.y, self.width - 20, self.height + 20)


class Base:
    WIDTH = base_img.get_width()
    VEL = 5
    IMG = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window():
    win.fill((0, 0, 0))
    base.draw()
    for cactus in cacti:
        cactus.draw(win)

    dino.draw(win)
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    pygame.display.update()


font = pygame.font.SysFont("arial", 20, True)
dino = Dino(50, 350, 64, 64)
base = Base(FLOOR)
cacti = [Cactus(1300)]
run = True
speed = 0
score_count = 0
while run:
    clock.tick(150)

    score_count += 1
    if score_count > 40:
        score = score + 1
        score_count = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    base.move()
    for cactus in cacti:
        cactus.move()

        if dino.hitbox.colliderect(cactus.hitbox):
            run = False

        if not cactus.passed and cactus.x < dino.x:
            cactus.passed = True
            cacti.append(Cactus(1300))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not dino.isJump:
            dino.isJump = True

    draw_window()

pygame.quit()
