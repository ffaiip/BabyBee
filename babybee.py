import arcade

from models import Bee

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700


class BabyBeeGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)

        self.bee = Bee(100, 100)
        self.bee_sprite = arcade.Sprite('images/bee.png')
        self.background = arcade.load_texture(
            "images/background.jpg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.bee_sprite.draw()

    def update(self, delta):
        bee = self.bee

        bee.update(delta)
        self.bee_sprite.set_position(bee.x, bee.y)


if __name__ == '__main__':
    window = BabyBeeGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
