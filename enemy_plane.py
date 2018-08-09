''' Define enemy plane.
'''


from flying_object import FlyingExplosiveObject
from random import randint


class EnemyPlane(FlyingExplosiveObject):
    '''
    '''

    def _reset_location(self):
        ''' Overwrite.
        '''

        self.rect.left = randint(0, self._background_width - self.rect.width)
        self.rect.top = randint(-5 * self.rect.height, -self.rect.height)

    def __init__(self, background_size, image, explosion_images, blood, size=None):
        ''' Initialize an enemy plane.
        '''

        super().__init__(background_size, image, explosion_images, blood, size)
        self._speed = 5
        self._reset_location()

    def update(self):
        if self._blood <= 0:
            self._killed = True

        if not self._killed:
            # If alive...
            if self.rect.top < self._background_height:
                self.rect.top += self._speed
            else:
                self._reset_location()
            self._trace_current_location_before_explosion()
        else:
            self._explode()

    def lose_blood(self, damage):
        self._blood -= damage


class FirstTierEnemyPlane(EnemyPlane):

    def __init__(self, background_size, image, explosion_images, blood, size=None):
        super().__init__(background_size, image, explosion_images, blood, size)
        self._blood = 2
