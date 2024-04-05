import pygame


def main():
    pygame.init()
    while not pygame.event.get().type == pygame.QUIT:
        pass
    pygame.quit()
    pass


if __name__ == "__main__":
    main()
