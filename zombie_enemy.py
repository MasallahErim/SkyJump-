from pgzero.actor import Actor
import random

class ZombieEnemy(Actor):
    def __init__(self, pos):
        super().__init__('zombie_idle', pos)
        self.run_frames = ['zombie_walk1', 'zombie_walk2']
        self.frame_index = 0.0
        self.speed = random.uniform(2.5, 5.5)

    def update(self):
        self.x -= self.speed
        self.frame_index = (self.frame_index + 0.2) % len(self.run_frames)
        self.image = self.run_frames[int(self.frame_index)]
