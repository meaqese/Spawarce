import pygame

from modules.helpers import load_image, terminate


def system_font(size):
    return pygame.font.Font('fonts/pssystem-regular.ttf', size)


def create_button(screen, name, num=1):
    margin_for_button = 100
    button_x, button_y = screen.get_width() // 2 - 250 // 2, \
                         screen.get_height() // 2 + \
                         (num - 1) * margin_for_button,
    screen.fill((55, 0, 110), (button_x, button_y, 250, 80))
    text = system_font(40).render(name, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.top = button_y + 20
    text_rect.x = screen.get_width() // 2 - text.get_width() // 2
    screen.blit(text, text_rect)

    return text_rect


def start_screen(screen: pygame.Surface, heading='Spawarce',
                 playtext='Start Game'):
    background = load_image('space.png')
    screen.blit(background, (0, 0))

    game_name = system_font(200).render(heading, True, (75, 0, 130))
    game_name_rect = game_name.get_rect()
    game_name_rect.top = screen.get_height() // 2 - 200
    game_name_rect.x = screen.get_width() // 2 - game_name.get_width() // 2
    screen.blit(game_name, game_name_rect)

    start_button = create_button(screen, playtext, 1)
    quit_button = create_button(screen, 'Quit', 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False
                elif quit_button.collidepoint(event.pos):
                    terminate()
        pygame.display.flip()

