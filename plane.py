''' Define base Plane class.
'''

from flying_object import FlyingExplosiveObject


class Plane(FlyingExplosiveObject):

    def _reset_location(self):
        raise NotImplementedError('define specific _reset_location')

    def _reset_after_explosion(self):
        ''' Overwrite this method.
        '''

        super()._reset_after_explosion()
        self._power = self._origin_power
        self._level = self._origin_level

    def __init__(self, background_size, image, explosion_images, lasers, laser_groups, blood, hit_damage, size=None):
        super().__init__(background_size, image, explosion_images, blood, hit_damage, size)
        self._power = 0
        self._level = 0
        self._origin_level = self._level
        self._origin_power = self._power
        self._lasers = lasers
        self._laser_groups = laser_groups
