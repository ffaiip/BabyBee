import arcade

from models import World, Bee

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()


class BabyBeeGameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(width, height)
        # self.bullet_list = None
        self.bee_sprite = ModelSprite('images/bee.png', model=self.world.bee)
        self.monster_sprite = ModelSprite('images/monster.png', model=self.world.monster)
        self.bullet_sprite = ModelSprite('images/bullet.png', model=self.world.bullet)

        self.background = arcade.load_texture("images/background.jpg")

    def setup(self):
        self.bullet_list = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.bullet_sprite.draw()
        # self.bullet_list.draw()                              
        self.bee_sprite.draw()
        self.monster_sprite.draw()
        

    def update(self, delta):
        self.world.update(delta)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)


if __name__ == '__main__':
    window = BabyBeeGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
