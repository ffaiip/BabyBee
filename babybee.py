import arcade

from models import World, Bee
import random
from coldetect import hit

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
MONSTER_COUNT = 1

MONSTER_SPEED = -3

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
        self.w = width
        self.h = height
        self.set_up(self.w, self.h)

    def set_up(self,width, height):
        arcade.set_background_color(arcade.color.BLACK)
        self.main_menu = {'over':arcade.load_texture("images/over.png"), 'start':arcade.load_texture("images/start.png")}
        self.world = World(width, height)
        self.bullet_list = arcade.SpriteList()
        self.bee_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.monster_list= arcade.SpriteList()
        self.bee_sprite = ModelSprite('images/bee.png', model=self.world.bee)
        self.laser_sound = arcade.sound.load_sound("sounds/laser.wav")
        self.bee_list.append(self.bee_sprite)
        self.game_stop = False
        self.game_start = False
        self.background = arcade.load_texture("images/background.jpg")

    def on_draw(self):
        print(len(self.monster_list))
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        # self.bullet_sprite.draw()
        self.bullet_list.draw()
        self.bee_sprite.draw()
        self.monster_list.draw()
        self.coin_list.draw()
        self.bee_list.draw()
        arcade.draw_text("Score : " + str(self.world.score), self.width -
                         120, self.height - 30, arcade.color.GRAY_BLUE, 20)
        if(self.game_stop):
              arcade.draw_texture_rectangle(self.width//2, self.height//2 + 70, 200, 100, self.main_menu['over'], 0, 255)

        if(self.game_start):
            arcade.draw_texture_rectangle(self.width//2, self.height//2 - 40, 100, 100, self.main_menu['start'], 0, 255)

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH)
        self.bullet_list.update()
        self.monster_list.update()


        for bullet in self.bullet_list:

            hit_list = hit(bullet, self.monster_list)

            if len(hit_list) > 0:
                self.coin_sprite = ModelSprite('images/coin.png', model=self.world.coin)

                self.coin_sprite.center_x = hit_list[0].center_x
                self.coin_sprite.center_y = hit_list[0].center_y

                self.coin_list.append(self.coin_sprite)
                self.coin_sprite.change_y = COIN_SPEED

                bullet.kill()

            for monster in hit_list:
                monster.kill()
        

        self.coin_list.update()

        for coin in self.coin_list:
            hit_list = hit(coin, self.bee_list)
            if len(hit_list) > 0:
                self.world.score += 1
                
                coin.kill()

        for monster in self.monster_list:

            hit_list = hit(monster, self.bee_list)

            if len(hit_list) > 0:
                
                self.game_stop = True
                self.game_start = True

            for bee in hit_list:
                bee.kill()

    def on_mouse_press(self, x, y, button, modifiers):
        menu = self.main_menu['start']
        h = SCREEN_HEIGHT//2 - 100
        w = SCREEN_WIDTH//2
        if w - menu.width//2 <= x <= w + menu.width//2:
            if h - menu.height//2 <= y <= h + menu.height//2:
                self.set_up(self.w, self.h)
                    




    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

        if key == arcade.key.SPACE:
            arcade.sound.play_sound(self.laser_sound)

            self.bullet_sprite = ModelSprite('images/bullet.png', model=self.world.bullet)

            self.bullet_sprite.change_y = BULLET_SPEED

            self.bullet_sprite.center_x = self.bee_sprite.center_x
            self.bullet_sprite.bottom = self.bee_sprite.top

            self.bullet_list.append(self.bullet_sprite)

        if key == arcade.key.ENTER:
            
            self.monster_sprite = ModelSprite('images/monster.png', model=self.world.monster)

            self.monster_sprite.change_y = MONSTER_SPEED

            self.monster_sprite.center_x = random.randint(30, SCREEN_WIDTH-30)
            self.monster_sprite.center_y = SCREEN_HEIGHT

            self.monster_list.append(self.monster_sprite)


if __name__ == '__main__':
    window = BabyBeeGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
