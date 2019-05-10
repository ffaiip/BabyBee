import arcade

def hit(player, competitor_list):
    return arcade.check_for_collision_with_list(player, competitor_list)