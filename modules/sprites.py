import pygame
from random import randint

from modules.helpers import load_image
from modules.interfaces import start_screen
from settings import FPS

direction = {
    80: (-10, 0),
    79: (10, 0),
}

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
home_group = pygame.sprite.Group()


class Dashboard(pygame.sprite.Sprite):
    def __init__(self):
        super(Dashboard, self).__init__(all_sprites)

        self.count = 0

        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

    def update_count(self, count=1):
        text = pygame.font.Font(None, 30)\
            .render(f'Очков: {self.count + count}', True, (255, 255, 255))
        self.image = pygame.Surface(text.get_size())
        self.rect = self.image.get_rect()
        self.image.blit(text, text.get_rect())

        self.count += count

    def reset(self):
        self.count = -1
        self.update_count()

    @property
    def kills(self):
        return self.count


dashboard = Dashboard()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen, center):
        super().__init__(all_sprites)

        self.image = load_image('spaceship.gif')
        self.screen = screen
        self.stronger = False

        center = center - self.image.get_width() // 2
        self.rect = self.image.get_rect().move(center, 500)

    def update(self, *args, **kwargs) -> None:
        if any(list(args[0])):
            signal = list(args[0]).index(1)

            if signal in direction:
                to_add = direction[signal]
                if to_add:
                    self.rect = self.rect.move(to_add)
            elif signal == 44:
                if clock.tick() > 100:
                    fireball_center = self.image.get_width() // 2 - 6

                    Fireball(self.rect.x + fireball_center, self.rect.y)
                    if self.stronger:
                        Fireball(self.rect.x + fireball_center, self.rect.y)
        if dashboard.kills >= 20:
            self.stronger = True

            self.image = pygame.transform.scale(load_image('spaceship-2.png'), (113, 102))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, width, stronger=False):
        super(Enemy, self).__init__(all_sprites, enemy_group)

        image_choice = 'enemy.png' if not stronger else 'enemy-2.png'
        self.image = pygame.transform.scale(
            load_image(image_choice), (106, 106))
        self.screen = screen

        self.stronger = stronger
        self.speed = 100 if not stronger else 60
        self.health = 2 if not stronger else 10

        self.window_width = width

        enemy_width = self.image.get_width()
        random_x = randint(0, width - enemy_width)
        random_y = randint(-512, 0) if not stronger else 0
        self.rect = self.image.get_rect().move(random_x, random_y)

    def update(self, *args, **kwargs) -> None:
        self.rect = self.rect.move(0, self.speed / FPS)

        if ball := pygame.sprite.spritecollideany(self, fireball_group):
            self.health -= 1

            if self.stronger:
                ball.remove(fireball_group)
            else:
                side = 106 if self.rect.x + 106 * 2 < self.window_width \
                    else -106
                self.rect = self.rect.move(side, 10 / FPS)

            if self.health == 0:
                self.remove(all_sprites, enemy_group)

                score = 1 if not self.stronger else 2
                dashboard.update_count(score)
        elif pygame.sprite.spritecollideany(self, home_group):
            start_screen(self.screen, f'Score: {dashboard.kills}')
            self.kill()
            dashboard.reset()


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Fireball, self).__init__(fireball_group)

        self.image = pygame.transform.scale(pygame.transform.rotate(
            load_image('fireball.gif'), -90), (12, 30))
        self.rect = self.image.get_rect().move(x, y)

    def update(self, *args, **kwargs) -> None:
        self.rect = self.rect.move(0, -200 / FPS)

    def get_center(self):
        return self.image.get_width() // 2


class Home(pygame.sprite.Sprite):
    def __init__(self):
        super(Home, self).__init__(all_sprites, home_group)

        self.image = load_image('home.png')
        self.rect = self.image.get_rect().move(0, 622)

