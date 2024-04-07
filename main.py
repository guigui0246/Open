import pygame
from typing import Callable, Dict, List
from Player import Player
from map import Map
import debug as log
from debug import debug
from sprite import AnimatedSprite, Sprite

log.print_to_stderr = False
SIZE: tuple[int, int] = (256, 256)
SCALE_DIFF_MAX: float = 1.45
SPEED_VALUE: float = 0.3
MIN_SPEED: float = 0.3
SLOWDOWN: float = 1.65
FRAMERATE: int = 60
BACKGROUND: pygame.Color = pygame.Color(0x74, 0x74, 0x74)


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
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if isinstance(elem["player"], Player):
                    elem["player"].jump()
        debug(e)

    if (not pygame.event.get_blocked(pygame.KEYDOWN)):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if isinstance(elem["player"], Player):
                elem["player"].speed += SPEED_VALUE
        if keys[pygame.K_LEFT]:
            if isinstance(elem["player"], Player):
                elem["player"].speed -= SPEED_VALUE
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            if isinstance(elem["player"], Player):
                if elem["player"].speed > MIN_SPEED:
                    elem["player"].speed /= SLOWDOWN
                else:
                    elem["player"].speed = 0

    if isinstance(elem["player"], Player) and isinstance(elem["map"], Map):
        elem["player"].move(elem["map"])

    show: Callable[[pygame.Surface, pygame.Surface, tuple[int, int], tuple[int, int]], None]
    show = make_show(scale_x, scale_y, margin_x, margin_y)
    for e in elemToShow:
        e.show(show, screen)


def main():
    global BACKGROUND
    size: tuple[int, int] = SIZE
    tick: int = 0
    pygame.init()
    pygame.display.set_caption("Open")
    screen: pygame.Surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    clock: pygame.time.Clock = pygame.time.Clock()
    events: List[pygame.event.Event] = pygame.event.get()
    elem: Dict[str, Sprite] = {
        "first_room": Map("assets/first_room.png"),
        "player": Player(3, (150, 150)),
        "second_room": Map("assets/background_no_enemies.png"),
        "final_room": Map("assets/final_room.png"),
        "gros_cochon": Sprite("assets/gros_cochon.png"),
        "soucoupe_volante": Sprite("assets/soucoupe_volante.png"),
        "pti_robot": Sprite("assets/pti_robot.png"),
        "porte_fin_ouverture": AnimatedSprite(["assets/pti_robot.png"], 3),
        "porte_fin": Sprite("assets/door_end_level.png"),
        "zombies": AnimatedSprite(["assets/zombie_sprite_1.png", "assets/zombie_sprite_2.png"], 3),
        "voleur": AnimatedSprite(["assets/voleur.png", "assets/voleur_2.png", "assets/voleur_3.png"], 3),
        "voleur_crowbar": AnimatedSprite(["assets/voleur_crowbar.png", "assets/voleur_crowbar_2.png", "assets/voleur_crowbar_3.png"], 3),
        "coffre1": AnimatedSprite(["assets/chest_front.png", "assets/chest_open_16x.png"], 1),
        "coffre2": AnimatedSprite(["assets/chest_front.png", "assets/chest_open_16x.png"], 1/2),
        "coffre3": AnimatedSprite(["assets/chest_front.png", "assets/chest_open_16x.png"], 1/3),
        "coffre4": AnimatedSprite(["assets/chest_front.png", "assets/chest_open_16x.png"], 1/4),
    }
    if isinstance(elem["first_room"], Map):
        elem["first_room"].collisions = [pygame.Rect(-200, -200, 2000, 2000)]
    if isinstance(elem["second_room"], Map):
        elem["second_room"].collisions = [
            pygame.Rect(-200, 255, 2000, 2000),
            pygame.Rect(-200, -200, 200, 2000),
            pygame.Rect(255, -200, 2000, 2000),
            pygame.Rect(0, 225, 67, 30),
            pygame.Rect(0, 194, 33, 30),
            pygame.Rect(70, 180, 34, 5),
            pygame.Rect(120, 168, 41, 5),
            pygame.Rect(179, 172, 76, 22),
            pygame.Rect(183, 131, 25, 14),
            pygame.Rect(224, 103, 20, 11),
            pygame.Rect(165, 85, 17, 5),
            pygame.Rect(0, 72, 146, 10),
        ]
    if isinstance(elem["final_room"], Map):
        elem["final_room"].collisions = [
            pygame.Rect(-200, 255, 2000, 2000),
            pygame.Rect(-200, -200, 200, 2000),
            pygame.Rect(255, -200, 2000, 2000),
        ]
    elem["zombies"].pos = (68, 226)
    elem["zombies"].size = (32, 32)
    elem["soucoupe_volante"].pos = (132, 130)
    elem["soucoupe_volante"].size = (16, 11)
    elem["pti_robot"].pos = (219, 139)
    elem["pti_robot"].size = (31, 33)
    elem["gros_cochon"].pos = (81, 40)
    elem["gros_cochon"].size = (32, 32)
    elem["porte_fin"].pos = (7, 47)
    elem["porte_fin"].size = (32, 25)
    elem["voleur_crowbar"].pos = (8, 225)
    elem["voleur"].pos = (194, 225)
    elem["coffre1"].pos = (28, 244)
    elem["coffre2"].pos = (72, 244)
    elem["coffre3"].pos = (120, 244)
    elem["coffre4"].pos = (166, 244)
    elem["player"].pos = (214, 244)
    elem["voleur_crowbar"].size = (32, 32)
    elem["voleur"].size = (32, 32)
    elem["coffre1"].size = (16, 12)
    elem["coffre2"].size = (16, 12)
    elem["coffre3"].size = (16, 12)
    elem["coffre4"].size = (16, 12)
    elem["player"].size = (16, 12)
    elem["voleur"].reverse = True
    elem["map"] = elem["first_room"]
    pygame.event.set_blocked(pygame.KEYDOWN)
    pygame.event.set_allowed(pygame.QUIT)
    elemToShow: List[Sprite] = [elem["map"]]
    elemToShow.append(elem["player"])
    elemToShow.append(elem["coffre1"])
    elemToShow.append(elem["coffre2"])
    elemToShow.append(elem["coffre3"])
    elemToShow.append(elem["coffre4"])
    elemToShow.append(elem["voleur_crowbar"])
    startboss: bool = False
    endboss: bool = False
    boss: bool = False
    while not len(list(filter(lambda a: a.type == pygame.QUIT, events))):
        size = screen.get_size()
        if tick == 1 * FRAMERATE:
            if isinstance(elem["coffre1"], AnimatedSprite):
                elem["coffre1"].framerate = 1 / 10
            elem["voleur_crowbar"].pos = (52, 225)
        if tick == 2 * FRAMERATE:
            if isinstance(elem["coffre2"], AnimatedSprite):
                elem["coffre2"].framerate = 1 / 10
            elem["voleur_crowbar"].pos = (100, 225)
        if tick == 3 * FRAMERATE:
            if isinstance(elem["coffre3"], AnimatedSprite):
                elem["coffre3"].framerate = 1 / 10
            elem["voleur_crowbar"].pos = (146, 225)
        if tick == 4 * FRAMERATE:
            if isinstance(elem["coffre4"], AnimatedSprite):
                elem["coffre4"].framerate = 1 / 10
            elem["voleur_crowbar"].pos = (194, 225)
        if tick == 4.25 * FRAMERATE:
            elemToShow.remove(elem["voleur_crowbar"])
            elemToShow.append(elem["voleur"])
        if tick == 4.4 * FRAMERATE:
            elem["voleur"].pos = (100, 225)
        if tick == 4.7 * FRAMERATE:
            elem["voleur"].pos = (75, 225)
        if tick == 4.9 * FRAMERATE:
            elem["voleur"].pos = (-5, 225)
        if tick == 5 * FRAMERATE:
            elem["map"] = elem["second_room"]
            elemToShow[0] = elem["map"]
            pygame.event.set_allowed(pygame.KEYDOWN)
            elem["player"].pos = (230, 230)
            elemToShow.remove(elem["coffre1"])
            elemToShow.remove(elem["coffre2"])
            elemToShow.remove(elem["coffre3"])
            elemToShow.remove(elem["coffre4"])
            elemToShow.remove(elem["voleur"])
            elemToShow.append(elem["zombies"])
            elemToShow.append(elem["soucoupe_volante"])
            elemToShow.append(elem["pti_robot"])
            elemToShow.append(elem["gros_cochon"])
            elemToShow.append(elem["porte_fin"])
        if startboss:
            elem["voleur"].reverse = False
            elem["voleur"].pos = (32, 232)
            elem["player"].pos = (209, 239)
            elemToShow.remove(elem["zombies"])
            elemToShow.remove(elem["soucoupe_volante"])
            elemToShow.remove(elem["pti_robot"])
            elemToShow.remove(elem["gros_cochon"])
            elemToShow.remove(elem["porte_fin"])
            elemToShow.append(elem["voleur"])
            startboss = False
            boss = True
        if endboss and tick > 5 * FRAMERATE:
            elemToShow.remove(elem["final_room"])
            elemToShow.remove(elem["voleur"])
            elemToShow.remove(elem["player"])
            elem["coffreFin"] = AnimatedSprite(["assets/chest_front.png", "assets/chest_open_16x.png"], 2)
            elem["coffreFin"].pos = (53, 53)
            elem["coffreFin"].size = (150, 150)
            elemToShow.append(elem["coffreFin"])
            tick = 0
        if endboss and tick == 1 * FRAMERATE:
            elem["voleur"].reverse = False
            elem["voleur"].pos = (32, 232)
            elem["player"].pos = (209, 239)
            elemToShow.remove(elem["coffreFin"])
            BACKGROUND = pygame.Color(255, 255, 255)
            elemToShow.append(Sprite("assets/hoppy.png"))
            tick = 0
        if boss:
            rect = pygame.Rect(32, 232, 32, 1)
            rect2 = pygame.Rect(elem["player"].pos, elem["player"].size)
            if rect.colliderect(rect2):
                endboss = True
                boss = False
        if elem["second_room"] in elemToShow:
            rect = pygame.Rect(elem["porte_fin"].pos, elem["porte_fin"].size)
            rect2 = pygame.Rect(elem["player"].pos, elem["player"].size)
            if rect.colliderect(rect2):
                startboss = True
        events = pygame.event.get()
        screen.fill(BACKGROUND)
        update_screen(screen, events, size, elem, elemToShow)
        pygame.display.flip()
        clock.tick(FRAMERATE)
        tick += 1
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
