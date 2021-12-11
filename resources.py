import pyglet

from utils.util import center_image

pyglet.resource.path = ["./resources"]
pyglet.resource.reindex()

background_image = pyglet.resource.image("background.png")
fireball_animation = pyglet.resource.animation("fireball.gif")
foreground_image = pyglet.resource.image("foreground.png")
ghost_idle_animation = pyglet.resource.animation("ghost_idle.gif")
ground_image = pyglet.resource.image("ground.png")
heart_image = pyglet.resource.image("heart.png")
icon_16_image = pyglet.resource.image("icon_16.png")
icon_32_image = pyglet.resource.image("icon_32.png")
player_attacking_animation = pyglet.resource.animation("player_attacking.gif")
player_falling_animation = pyglet.resource.animation("player_falling.gif")
player_idle_animation = pyglet.resource.image("player_idle.gif")
player_running_backward_animation = pyglet.resource.animation("player_running_backward.gif")
player_running_forward_animation = pyglet.resource.animation("player_running_forward.gif")
wolf_running = pyglet.resource.animation("wolf_running.gif")

center_image(fireball_animation)
center_image(ghost_idle_animation)
center_image(player_attacking_animation)
center_image(player_falling_animation)
center_image(player_idle_animation)
center_image(player_running_backward_animation)
center_image(player_running_forward_animation)
center_image(wolf_running)
heart_image.anchor_y = heart_image.height
