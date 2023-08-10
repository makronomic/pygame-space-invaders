import pygame
from random import randint

# initialize pygame
pygame.init()

# global const variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
NO_ENEMIES = 10

class Entity:
    image: pygame.surface.Surface = 0
    type: str = "" 
    x: float = 0
    y: float = 0
    speed: float = 0
    dx: float = 0

    def __init__(self, image: pygame.surface.Surface, type: str, x: float = 0, y: float = 0, speed: float = 0):
        self.image = image
        self.type = type
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = 0
 
def handle_movement(entity: Entity) -> None:
    match entity.type:
        case "Player":
            # get the activation state of every key
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                if keys[pygame.K_LEFT]:
                    entity.dx = -entity.speed

                if keys[pygame.K_RIGHT]:
                    entity.dx = entity.speed
    
            # stop, if key released
            else:
                entity.dx = 0
            
        case "Enemy":
            entity.dx = entity.speed

        case _:
            return

    # apply the change in the position
    entity.x += entity.dx

def out_of_bounds(entity: Entity) -> None:
    if entity.x > SCREEN_WIDTH: entity.x = 0
    if entity.x + entity.image.get_width() < 0: entity.x = SCREEN_WIDTH

    if entity.y > SCREEN_HEIGHT: entity.y = 0
    if entity.y < 0: entity.y = SCREEN_HEIGHT

def main():
    # setup the window, sprites, etc...
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    main_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")
    pygame.display.set_icon(pygame.image.load("Space Invaders/res/gameicon.png"))

    player = Entity(image=pygame.image.load("Space Invaders/res/player.png"), type="Player")
    player.x, player.y, player.speed = (SCREEN_WIDTH / 2) - player.image.get_width(), SCREEN_HEIGHT - player.image.get_height() - 10, 0.5 

    enemies: list[Entity] = []

    # spawn random enemies on the upper half of the screen
    for _ in range(NO_ENEMIES):
        enemies.append(Entity(image=pygame.image.load("Space Invaders/res/enemy.png"), type="Enemy", x=randint(0, SCREEN_WIDTH - 64), y=randint(0, SCREEN_HEIGHT) / 2, speed=0.7))

    # main game loop
    game_running = True
    while game_running:
        # event handling, per frame
        for event in pygame.event.get():
            # exit the game
            if event.type == pygame.QUIT:
                game_running = False

        # out of bounds checking for the entities
        out_of_bounds(player)
        for enemy in enemies:
            out_of_bounds(enemy)

        # handle continuous button holds, such as holding a movement key
        handle_movement(player)
        for enemy in enemies:
            handle_movement(enemy)

        # draw the player
        main_window.blit(player.image, (player.x, player.y))

        # draw all the enemies
        for enemy in enemies:
            main_window.blit(enemy.image, (enemy.x, enemy.y))

        # update the display
        pygame.display.update()
        main_window.fill((0,0,0))
    
    pygame.quit()

if __name__ == "__main__":
    main()