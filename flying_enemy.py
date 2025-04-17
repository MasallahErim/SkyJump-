from pgzero.actor import Actor
import random
import math

class FlyingEnemy(Actor):
    def __init__(self, pos):
        super().__init__('enemyflying_1', pos)
        self.fly_frames = ['enemyflying_1', 'enemyflying_2', 'enemyflying_3']
        self.frame_index = 0.0
        self.speed = random.uniform(3.0, 6.0)
        self.amplitude = random.uniform(10, 40)
        self.frequency = random.uniform(0.01, 0.03)
        self.base_y = pos[1]

    def update(self):
        self.x -= self.speed
        self.y = self.base_y + math.sin(self.x * self.frequency) * self.amplitude
        self.frame_index = (self.frame_index + 0.2) % len(self.fly_frames)
        self.image = self.fly_frames[int(self.frame_index)]
