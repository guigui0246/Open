from typing import List
import pygame

SIZE: tuple[int, int] = (256, 256)
SCALE_DIFF_MAX: float = 0.1


def update_screen(screen: pygame.Surface, events: List[pygame.event.Event], size: tuple[int, int]):
    margin_x: int = 0
    margin_y: int = 0
    scale_x: float = size[0] / SIZE[0]
    scale_y: float = size[1] / SIZE[1]
    if size[1] > size[0]:
        while scale_y / scale_x > SCALE_DIFF_MAX:
            margin_y += 1
            scale_y = (size[1] - (2 * margin_y)) / SIZE[1]
    else:
        while scale_x / scale_y > SCALE_DIFF_MAX:
            margin_x += 1
            scale_x = (size[0] - (2 * margin_x)) / SIZE[0]


def main():
    size: tuple[int, int] = SIZE
    pygame.init()
    pygame.display.set_caption("Open")
    screen: pygame.Surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    clock: pygame.time = pygame.time.Clock()
    events: List[pygame.event.Event] = pygame.event.get()
    while not len(list(filter(lambda a: a.type == pygame.QUIT, events))):
        size = screen.get_size()
        events = pygame.event.get()
        screen.fill("white")
        update_screen(screen, events, size)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
