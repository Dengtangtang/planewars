''' Define supplies.
'''

from flying_object import FlyingObject
from random import randint


class Supply(FlyingObject):

    def _reset_location(self):
        self._picked = False
        self.rect.left = randint(0 + self._sidesway, self._background_width - self.rect.width - self._sidesway)
        self.rect.top = randint(-5 * self.rect.height, -self.rect.height)

    def _move_sprial(self):
        self.rect.top += self._speed
        if not (self._sidesway_delay % 5):
            if self._sidesway_left:
                self.rect.left -= self._sidesway
            else:
                self.rect.left += self._sidesway
            self._sidesway_left = not self._sidesway_left
        self._sidesway_delay -= 1
        if self._sidesway_delay <= 0:
            self._sidesway_delay = 100

    def __init__(self, background_size, image, size=None):
        super().__init__(background_size, image, size)
        self._speed = 5
        self._sidesway = 20
        self._sidesway_delay = 100
        self._sidesway_left = True
        self._picked = False

        self._reset_location()

    def update(self):
        self.rect.top += self._speed
        # self._move_sprial()
        if self.rect.top >= self._background_height or self._picked:
            # self.kill()  # WILL USE THIS WHEN I USE TIME CONTROLLER.
            self._reset_location()

    def set_picked(self):
        self._picked = True
