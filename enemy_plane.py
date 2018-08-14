''' Define enemy plane.
'''

from pygame.math import Vector2
from plane import Plane
from weapon import EnemyLaser
from random import randint


class Enemy(Plane):

    _y_offset = -10

    def _reset(self):
        super()._reset()
        self.rect.left = randint(0, self._screen_width - self.rect.width)
        self.rect.top = randint(self._y_offset * self.rect.height, -self.rect.height)

    def _update_when_not_killed_hook(self):
        if self.rect.top < self._screen_height:
            self.rect.top += self._speed
        else:
            self._reset()

        if self.rect.top > 0:
            self._fire_process()

    def _update_when_killed_hook(self):
        self._reset()

    def _fire(self):
        for i in range(self._level + 1):
            laser = EnemyLaser((self._screen_width, self._screen_height),
                               self._lasers[self._power],
                               self.rect,
                               self._level,
                               self._laser_speed,
                               self._laser_damage,
                               self._fire_positions[i],
                               self._laser_size)
            for gp in self._laser_groups:
                gp.add(laser)

    def __init__(self, screen_size, image, lasers, laser_groups, size=None):
        super().__init__(screen_size, image, lasers, laser_groups, size)

        # Init.
        self._reset()

    def get_score(self):
        return self._score


class ElementaryEnemy(Enemy):

    _fire_delay_factor = 50

    def __init__(self, screen_size, image, lasers, laser_groups, size=None):
        super().__init__(screen_size, image, lasers, laser_groups, size)
        self._score = 200
        self._speed = 7  # May be overwritten subclass objects.
        self._blood = 3  # May be overwritten subclass objects.
        self._origin_blood = self._blood  # May be overwritten subclass objects.
        self._strike = 3  # May be overwritten subclass objects.
        self._laser_speed = 10
        self._laser_damage = 1
        self._laser_size = (15, 15)
        self._fire_positions = ['center']


class MidEnemy(Enemy):

    _fire_delay_factor = 40

    def __init__(self, screen_size, image, lasers, laser_groups, size=None):
        super().__init__(screen_size, image, lasers, laser_groups, size)
        self._score = 300
        self._speed = 6  # May be overwritten subclass objects.
        self._blood = 6  # May be overwritten subclass objects.
        self._origin_blood = self._blood  # May be overwritten subclass objects.
        self._strike = 4  # May be overwritten subclass objects.
        self._laser_speed = 10
        self._laser_damage = 2
        self._laser_size = (9, 30)
        self._fire_positions = ['center']


class AdvancedEnemy(Enemy):
    ''' UFOs.
    '''
    _fire_delay_factor = 30

    def __init__(self, screen_size, image, lasers, laser_groups, size=None):
        super().__init__(screen_size, image, lasers, laser_groups, size)
        self._score = 500
        self._speed = 5  # May be overwritten subclass objects.
        self._blood = 12  # May be overwritten subclass objects.
        self._origin_blood = self._blood  # May be overwritten subclass objects.
        self._strike = 5  # May be overwritten subclass objects.
        self._level = 1  # May be overwritten subclass objects.
        self._origin_level = self._level  # May be overwritten subclass objects.
        self._laser_speed = 10
        self._laser_damage = 3
        self._laser_size = (9, 30)
        self._fire_positions = ['left', 'right']


class Meteor(Enemy):

    def __init__(self, screen_size, image, lasers, laser_groups, size=None):
        super().__init__(screen_size, image, lasers, laser_groups, size)
        self._speed = 15
        self._strike = 5
        self._score = 100

        dest = Vector2(randint(0, self._screen_width - self.rect.width), self._screen_height)
        source = Vector2(self.rect.left, self.rect.top)
        dist = source.distance_to(dest)
        self._speedx = (dest[0] - source[0]) / dist * self._speed
        self._speedy = (dest[1] - source[1]) / dist * self._speed

    def _update_when_not_killed_hook(self):

        if self.rect.top >= self._screen_height:
            self._reset()
        else:
            self.rect.top += self._speedy
            self.rect.left += self._speedx
