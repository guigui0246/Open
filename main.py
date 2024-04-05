import pygame

SIZE: tuple[int, int] = (1280, 720)
size: tuple[int, int] = SIZE


def main():
    global size
    pygame.init()
    pygame.display.set_caption("Open")
    screen: pygame.Surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    clock: pygame.time = pygame.time.Clock()
    while not len(list(filter(lambda a: a.type == pygame.QUIT, pygame.event.get()))):
        size = screen.get_size()
        screen.fill("white")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
