import arcade.key

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}

MOVEMENT_SPEED = 4


class Bee:
    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.angle = 0

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.move(self.direction)


class Monster:

    MONSTER_SPEED = 1

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def update(self, delta):
        self.y -= Monster.MONSTER_SPEED


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bee = Bee(self, 100, 100)
        self.monster = Monster(self, width-200, height)

    def update(self, delta):
        self.bee.update(delta)
        self.monster.update(delta)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.bee.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.bee.direction = DIR_RIGHT
