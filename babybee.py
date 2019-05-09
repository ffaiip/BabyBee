import arcade

from models import World, Bee
import random
from coldetect import hit

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
MONSTER_COUNT = 5

MONSTER_SPEED = -1

COIN_SPEED = -5

BULLET_SPEED = 5


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
        self.bullet_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.bee_sprite = ModelSprite('images/bee.png', model=self.world.bee)
        # self.monster_sprite = ModelSprite(
        #     'images/monster.png', model=self.world.monster)
        # self.bullet_sprite = ModelSprite(
        #     'images/bullet.png', model=self.world.bullet)

        self.laser_sound = arcade.sound.load_sound("sounds/laser.wav")

        # Create the monsters
        for monster in range(MONSTER_COUNT):

            monster = ModelSprite('images/monster.png',
                                  model=self.world.monster)

            monster.center_x = random.randint(30, SCREEN_WIDTH-30)
            monster.center_y = SCREEN_HEIGHT

            monster.change_y = MONSTER_SPEED

            self.monster_list.append(monster)

        self.background = arcade.load_texture("images/background.jpg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        # self.bullet_sprite.draw()
        self.bullet_list.draw()
        self.bee_sprite.draw()
        self.monster_list.draw()
        # self.monster_sprite.draw()
        self.coin_list.draw()

        arcade.draw_text("Score : " + str(self.world.score), self.width -
                         120, self.height - 30, arcade.color.GRAY_BLUE, 20)

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH)
        self.bullet_list.update()
        self.monster_list.update()

        for bullet in self.bullet_list:

            hit_list = hit(bullet, self.monster_list)

            if len(hit_list) > 0:
                print("ok")
                self.coin_sprite = ModelSprite(
                    'images/coin.png', model=self.world.coin)

                self.coin_sprite.center_x = hit_list[0].center_x
                self.coin_sprite.center_y = hit_list[0].center_y

                self.coin_list.append(self.coin_sprite)
                self.coin_sprite.change_y = COIN_SPEED

                print(len(self.coin_list))

                bullet.kill()

            for monster in hit_list:
                monster.kill()

        self.coin_list.update()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

        if key == arcade.key.SPACE:
            arcade.sound.play_sound(self.laser_sound)

            self.bullet_sprite = ModelSprite(
                'images/bullet.png', model=self.world.bullet)

            self.bullet_sprite.change_y = BULLET_SPEED

            self.bullet_sprite.center_x = self.bee_sprite.center_x
            self.bullet_sprite.bottom = self.bee_sprite.top

            self.bullet_list.append(self.bullet_sprite)


if __name__ == '__main__':
    window = BabyBeeGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
