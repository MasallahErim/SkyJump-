import random
from pgzero.actor import Actor
from pgzero.loaders import sounds

WIDTH = 1200
HEIGHT = 720
CHAR_HALF = 120 / 2

class Hero(Actor):
    def __init__(self, pos):
        super().__init__('adventurer_stand', pos)
        self.idle_frames = ['adventurer_stand', 'adventurer_cheer1', 'adventurer_cheer2']
        self.run_frames = ['adventurer_walk1', 'adventurer_walk2']
        self.jump_frames = ['adventurer_jump']
        self.frame_index = 0.0
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.state = "idle"

    def update(self, sound_on, sound_volume):
        self.x += self.vx
        halfw = self._surf.get_width() / 2
        self.x = max(halfw, min(WIDTH - halfw, self.x))

        if not self.on_ground:
            self.vy += 0.4
            self.y += self.vy
            if self.y >= HEIGHT - CHAR_HALF:
                self.y = HEIGHT - CHAR_HALF
                self.vy = 0
                self.on_ground = True

        if not self.on_ground:
            self.state = "jump"
        elif self.vx != 0:
            self.state = "run"
        else:
            self.state = "idle"

        self.animate()

    def animate(self):
        self.frame_index = (self.frame_index + 0.2) % 3
        if self.state == "run":
            self.image = self.run_frames[int(self.frame_index) % len(self.run_frames)]
        elif self.state == "jump":
            self.image = self.jump_frames[0]
        else:
            self.image = self.idle_frames[int(self.frame_index) % len(self.idle_frames)]

    def jump(self, sound_on, sound_volume):
        if self.on_ground:
            self.vy = -12
            self.on_ground = False
            if sound_on:
                sounds.jump.set_volume(sound_volume)
                sounds.jump.play()
