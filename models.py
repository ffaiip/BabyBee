import arcade.key
from random import randint

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}

MOVEMENT_SPEED = 4

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700


class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0


class Bee(Model):
    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1

    def __init__(self, world, x, y):
        super().__init__(world, x, y, -90)

        self.direction = DIR_STILL

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.move(self.direction)

class Monster(Model):

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)


class Coin(Model):

    # COIN_SPEED = 1

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    # def update(self, delta):
    #     self.y -= Coin.COIN_SPEED


class Bullet(Model):

    BULLET_SPEED = 3

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    # def update(self, delta):
    #     self.y += Bullet.BULLET_SPEED


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bee = Bee(self, 100, 100)
        self.monster = Monster(self, 100, 100)
        # self.monster =[ Monster(self, width - 100, height),
        #     Monster(self, width - 200, height + 100),
        #     Monster(self, width - 250, height + 200),
        #     Monster(self, width - 300, height + 300),
        #     Monster(self, width - 200, height + 400)]
        self.bullet = Bullet(self, 100, 101)
        self.coin = Coin(self, 100, height+50)
        self.score = 0

    def update(self, delta):
        self.bee.update(delta)
        
    def limit_screen(self, width):
        if self.bee.x >= width - 30:
            self.bee.x = width - 30
        elif self.bee.x <= 30:
            self.bee.x = 30
        
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.bee.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.bee.direction = DIR_RIGHT
