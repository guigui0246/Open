import pygame
from typing import Callable, Dict, List
from Player import Player
from map import Map
import debug as log
from debug import debug
from sprite import Sprite

log.print_to_stderr = False
SIZE: tuple[int, int] = (256, 256)
SCALE_DIFF_MAX: float = 1.45
SPEED_VALUE = 1.25


def make_show(scale_x: float, scale_y: float, margin_x: int, margin_y: int) -> Callable[
              [pygame.Surface, pygame.Surface, tuple[int, int], tuple[int, int]], None]:
    def _show(screen: pygame.Surface, elem: pygame.Surface, coords: tuple[int, int], size: tuple[int, int]) -> None:
        coords = (int(scale_x * coords[0] + margin_x), int(scale_y * coords[1] + margin_y))
        size = (int(scale_x * size[0]), int(scale_y * size[1]))
        debug("Show Rect (Size (", size, "), Coords (", coords, "))")
        screen.blit(pygame.transform.scale(elem, size), coords)
    return _show


def update_screen(screen: pygame.Surface, events: List[pygame.event.Event], size: tuple[int, int],
                  elem: Dict[str, Sprite], elemToShow: List[Sprite]):
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
    debug("Margin (", margin_x, margin_y, "), Scale (", scale_x, scale_y, ")")

    for e in events:
        if e.type == pygame.K_SPACE:
            if isinstance(elem["player"], Player):
                elem["player"].jump()
        if e.type == pygame.K_RIGHT:
            if isinstance(elem["player"], Player):
                elem["player"].speed += SPEED_VALUE
        if e.type == pygame.K_LEFT:
            if isinstance(elem["player"], Player):
                elem["player"].speed -= SPEED_VALUE

    if isinstance(elem["player"], Player) and isinstance(elem["map"], Map):
        elem["player"].move(elem["map"])

    show: Callable[[pygame.Surface, pygame.Surface, tuple[int, int], tuple[int, int]], None]
    show = make_show(scale_x, scale_y, margin_x, margin_y)
    for e in elemToShow:
        e.show(show, screen)


def main():
    size: tuple[int, int] = SIZE
    pygame.init()
    pygame.display.set_caption("Open")
    screen: pygame.Surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    clock: pygame.time.Clock = pygame.time.Clock()
    events: List[pygame.event.Event] = pygame.event.get()
    elem: Dict[str, Sprite] = {
        "first_room": Sprite("assets/first_room.png"),
        "player": Player(3, (150, 150)),
        "map": Map("assets/first_room.png"),
    }
    if isinstance(elem["map"], Map):
        elem["map"].collisions = [pygame.Rect(50, 200, 15, 3)]
    elem["player"].size = (50, 50)
    elemToShow: List[Sprite] = []
    elemToShow.append(elem["map"])
    elemToShow.append(elem["player"])
    while not len(list(filter(lambda a: a.type == pygame.QUIT, events))):
        size = screen.get_size()
        events = pygame.event.get()
        screen.fill("white")
        update_screen(screen, events, size, elem, elemToShow)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
