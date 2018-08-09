''' Define enemy plane.
'''


from plane import Plane
from weapon import EnemyLaser
from random import randint


class EnemyPlane(Plane):
    '''
    '''

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        ''' Initialize an enemy plane.
        '''

        super().__init__(background_size, image, explosion_images, lasers, groups, blood, size)
        self._speed = 5
        self._reset_location()


class FirstTierEnemyPlane(EnemyPlane):

    def _reset_location(self):
        ''' Overwrite this method.
        '''

        self.rect.left = randint(0, self._background_width - self.rect.width)
        self.rect.top = randint(-5 * self.rect.height, -self.rect.height)

    def _fire(self):
        laser_speed = 10
        laser_damage = 1
        laser_size = (9, 30)
        for i in range(self._level + 1):
            laser = EnemyLaser((self._background_width, self._background_height),
                               self._lasers[self._power],
                               self.rect,
                               self._level,
                               laser_speed,
                               laser_damage,
                               'center',
                               laser_size)
            for gp in self._groups:
                gp.add(laser)

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        super().__init__(background_size, image, explosion_images, lasers, groups, blood, size)
        self._blood = 2
        self._fire_laser_delay = 500

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
            if not (self._fire_laser_delay % 50):
                self._fire()
            self._fire_laser_delay -= 1
            if self._fire_laser_delay <= 0:
                self._fire_laser_delay = 100
        else:
            self._explode()
