''' Define enemy plane.
'''


from plane import Plane
from weapon import EnemyLaser
from random import randint


class EnemyPlane(Plane):
    '''
    '''

    _y_offset = -10

    def _reset_location(self):
        ''' Overwrite this method.
        '''

        self._blood = self._origin_blood
        self.rect.left = randint(0, self._background_width - self.rect.width)
        self.rect.top = randint(self._y_offset * self.rect.height, -self.rect.height)

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        ''' Initialize an enemy plane.
        '''

        super().__init__(background_size, image, explosion_images, lasers, groups, blood, size)
        self._speed = 5
        self._fire_laser_delay = 500
        self._reset_location()

    def update(self):
        if self._blood <= 0:
            self._killed = True

        if not self._killed:
            # If alive...
            # Move...
            if self.rect.top < self._background_height:
                self.rect.top += self._speed
            else:
                self._reset_location()
            self._trace_current_location_before_explosion()

            # Fire...
            if self.rect.top > 0:
                if not (self._fire_laser_delay % 50):
                    self._fire()
                self._fire_laser_delay -= 1
                if self._fire_laser_delay <= 0:
                    self._fire_laser_delay = 100
        else:
            self._explode()


class FirstTierEnemyPlane(EnemyPlane):

    def _fire(self):
        for i in range(self._level + 1):
            laser = EnemyLaser((self._background_width, self._background_height),
                               self._lasers[self._power],
                               self.rect,
                               self._level,
                               self._laser_speed,
                               self._laser_damage,
                               self._lasers[-1],
                               'center',
                               self._laser_size)
            for gp in self._groups:
                gp.add(laser)

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        super().__init__(background_size, image, explosion_images, lasers, groups, blood, size)
        self._laser_speed = 10
        self._laser_damage = 1
        self._laser_size = (15, 15)


class SecondTierEnemyPlane(FirstTierEnemyPlane):

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        super().__init__(background_size, image, explosion_images, lasers, groups, blood, size)
        self._laser_size = (9, 30)
        self._laser_damage = 2


class UFO(EnemyPlane):

    def _fire(self):
        positions = ['left', 'right']
        for i in range(self._level + 1):
            laser = EnemyLaser((self._background_width, self._background_height),
                               self._lasers[self._power],
                               self.rect,
                               self._level,
                               self._laser_speed,
                               self._laser_damage,
                               self._lasers[-1],
                               positions[i],
                               self._laser_size)
            for gp in self._groups:
                gp.add(laser)

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        super().__init__(background_size, image, explosion_images, lasers, groups, blood, size)
        self._laser_speed = 10
        self._laser_size = (9, 30)
        self._laser_damage = 3
        self._level = 1
        self._origin_level = self._level
