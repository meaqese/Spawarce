from modules.sprites import *
from modules.helpers import terminate, load_image
from modules.interfaces import start_screen

pygame.init()

width, height = 960, 672
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Spawarce')
clock = pygame.time.Clock()

SPAWN_EVENT = pygame.USEREVENT + 1
SPAWN_STRONGER_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_EVENT, 3000)
pygame.time.set_timer(SPAWN_STRONGER_EVENT, 10000)

background = load_image('space.png')

spaceship = Spaceship(screen, width // 2)
enemy = Enemy(screen, width)
home = Home()

start_screen(screen)

while True:
    screen.blit(background, (randint(0, 1), randint(0, 1)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                start_screen(screen, playtext='Resume')
        elif event.type == SPAWN_EVENT:
            Enemy(screen, width)
        elif event.type == SPAWN_STRONGER_EVENT:
            Enemy(screen, width, stronger=True)
    all_sprites.update(pygame.key.get_pressed())
    all_sprites.draw(screen)

    fireball_group.update()
    fireball_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

