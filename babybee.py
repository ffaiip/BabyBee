import arcade

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class SpaceGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.bee = arcade.Sprite('images/bee.png')
        self.bee.set_position(100, 100)

    def on_draw(self):
        arcade.start_render()

        self.bee.draw()

    def update(self, delta):
        bee = self.bee

        if bee.center_y > SCREEN_HEIGHT:
            bee.center_y = 0
        bee.set_position(bee.center_x, bee.center_y + 5)


if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
