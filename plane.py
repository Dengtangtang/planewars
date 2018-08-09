''' Define base Plane class.
'''

from flying_object import FlyingExplosiveObject


class Plane(FlyingExplosiveObject):

    def _reset_location(self):
        raise NotImplementedError('define specific _reset_location')

    def _reset_after_explosion(self):
        ''' Overwrite this method.
        '''

        self._killed = False
        self.image = self._origin_image
        self._blood = self._origin_blood
        self._power = 0
        self._level = 0
        self._reset_location()

    def __init__(self, background_size, image, explosion_images, lasers, groups, blood, size=None):
        super().__init__(background_size, image, explosion_images, blood, size)
        self._power = 0
        self._level = 0
        self._lasers = lasers
        self._groups = groups
