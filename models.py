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

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)


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

    MONSTER_SPEED = 1

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def update(self, delta):
        self.y -= Monster.MONSTER_SPEED

    def random_position(self):
        self.x = randint(0, self.world.width - 1)
        self.y = SCREEN_HEIGHT


class Coin(Model):

    COIN_SPEED = 1

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def update(self, delta):
        self.y -= Coin.COIN_SPEED


class Bullet(Model):

    BULLET_SPEED = 3

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def update(self, delta):
        self.y += Bullet.BULLET_SPEED


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bee = Bee(self, 100, 100)
        self.monster = Monster(self, 100, height)
        self.bullet = Bullet(self, 100, 101)
        self.coin = Coin(self, 100, height+50)
        self.score = 0

    def update(self, delta):
        self.bee.update(delta)
        self.monster.update(delta)
        self.bullet.update(delta)
        self.coin.update(delta)

        if self.bullet.hit(self.monster, 20):
            self.monster.random_position()
            self.bullet.y = 101

        if self.bee.hit(self.coin, 20):
            self.score += 1
            self.coin.y = SCREEN_HEIGHT

    # def on_mouse_press(self, x, y, button, modifiers):
    #     bullet = Bullet(self, 100, 200)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.bee.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.bee.direction = DIR_RIGHT
