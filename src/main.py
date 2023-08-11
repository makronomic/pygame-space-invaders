import pygame
from random import randint
from math import sqrt

# initialize pygame
pygame.init()

# global const variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
NO_ENEMIES = 5

class Bullet:
    image: pygame.surface.Surface = 0

    state: str = ""

    x: float = 0
    y: float = 0
    speed: float = 0
    dy: float = 0

    def __init__(self, image: pygame.surface.Surface, state: str = "ready", x: float = 0, y: float = 0, speed: float = 0):
        self.image = image
        self.state = state
        self.x = x
        self.y = y
        self.speed = speed
        self.dy = 0

class Entity:
    image: pygame.surface.Surface = 0

    type: str = "" 

    x: float = 0
    y: float = 0
    speed: float = 0
    dx: float = 0
    dy: float = 0

    alive: bool = True

    def __init__(self, image: pygame.surface.Surface, type: str, x: float = 0, y: float = 0, speed: float = 0):
        self.image = image
        self.type = type
        self.x = x
        self.y = y
        self.speed = speed
        self.dx = 0
        self.alive = True
    
    def prepare_bullet(self, bullet: Bullet) -> None:
        # only players can fire bullets
        if self.type is "enemy":
            return
        
        match bullet.state:
            case "ready":
                # set the bullet's position
                bullet.x = self.x + (bullet.image.get_width() / 2)
                bullet.y = self.y - bullet.image.get_height()

                bullet.state = "fire"

            case "fire":
                pass

def collide(entity: Entity, bullet: Bullet) -> bool:
    return sqrt((entity.x - bullet.x) ** 2 + (entity.y - bullet.y) ** 2) <= 5

def out_of_bounds(entity: Entity) -> None:
    match entity.type:
        case "Player":
            if entity.x > SCREEN_WIDTH: entity.x = 0
            if entity.x + entity.image.get_width() < 0: entity.x = SCREEN_WIDTH

            if entity.y > SCREEN_HEIGHT: entity.y = 0
            if entity.y < 0: entity.y = SCREEN_HEIGHT

            return
            
        case "Enemy":
            # bounce the enemy off the wall by inverting the direction of its motion
            if entity.x + entity.image.get_width() >= SCREEN_WIDTH or entity.x <= 0:
                entity.speed *= -1

            return

def handle_bullet_movement(bullet: Bullet, screen: pygame.surface.Surface) -> None:
    match bullet.state:
        case "ready":
            pass

        case "fire":
            # draw the bullet
            screen.blit(bullet.image, (bullet.x, bullet.y))

            # assumes the bullet is already at the head of the spaceship
            bullet.dy = -bullet.speed

    # apply the change in the position
    bullet.y += bullet.dy

def is_alive(entity: Entity, bullet: Bullet) -> None:
    # player doesn't "die"
    if entity.type is "player":
        return
    
    if collide(entity, bullet):
        entity.alive = False
    
def draw(entity: Entity, window: pygame.surface.Surface) -> None:
    if entity.alive:
        window.blit(entity.image, (entity.x, entity.y))

def handle_entity_movement(entity: Entity) -> None:
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
            if entity.alive:
                entity.dx = entity.speed

                # get the enemies closer to the player
                entity.dy = 0.1

        case _:
            return

    # apply the change in the position
    entity.x += entity.dx
    entity.y += entity.dy

def reset_bullet(bullet: Bullet, enemies: list[Entity]) -> None:
    # 1st case: bullet didn't hit any enemy and went out of bounds
    if bullet.y <= 0:
        bullet.state = "ready"

        return 
    
    # 2nd case: bullet hit an enemy, WIP
    for enemy in enemies:
        if collide(entity=enemy, bullet=bullet):
            bullet.state = "ready"


def main():
    # setup the window, sprites, etc...
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    main_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # images
    bg_img = pygame.image.load("Space Invaders/res/background.png")
    player_img = pygame.image.load("Space Invaders/res/player.png")
    enemy_img = pygame.image.load("Space Invaders/res/enemy.png")
    game_icon_img = pygame.image.load("Space Invaders/res/gameicon.png")
    bullet_img = pygame.image.load("Space Invaders/res/bullet.png")

    pygame.display.set_caption("Space Invaders")
    pygame.display.set_icon(game_icon_img)

    # player
    player = Entity(image=player_img, type="Player")
    player.x, player.y, player.speed = (SCREEN_WIDTH / 2) - player.image.get_width(), SCREEN_HEIGHT - player.image.get_height() - 10, 2 

    # enemies
    enemies: list[Entity] = []

    # spawn random enemies on the upper half of the screen
    for _ in range(NO_ENEMIES):
        enemies.append(Entity(image=enemy_img, type="Enemy", x=randint(0, SCREEN_WIDTH - 64), y=randint(0, SCREEN_HEIGHT) / 2, speed=1.4))

    # bullet
    bullet = Bullet(image=bullet_img, speed=2)

    # main game loop
    game_running = True
    while game_running:
        # background image
        main_window.blit(bg_img, (0,0))

        # event handling, per frame
        for event in pygame.event.get():
            # exit the game
            if event.type == pygame.QUIT:
                game_running = False
                
            # preparing a bullet to be fired
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.prepare_bullet(bullet)

        # out of bounds checking for the entities
        out_of_bounds(player)
        for enemy in enemies:
            out_of_bounds(enemy)

        # handle continuous button holds, such as holding a movement key
        handle_entity_movement(player)
        for enemy in enemies:
            handle_entity_movement(enemy)

        # check for the bullet resetting
        reset_bullet(bullet=bullet, enemies=enemies)

        # handle the bullet firing mechanism
        handle_bullet_movement(bullet=bullet, screen=main_window)

        # checking if an enemy got hit after the bullet fired
        for enemy in enemies:
            is_alive(entity=enemy, bullet=bullet)

        ### DRAWING ###

        # draw the player
        draw(entity=player,window=main_window)

        # draw all the enemies
        for enemy in enemies:
            draw(entity=enemy,window=main_window)

        # update the display
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()