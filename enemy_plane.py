''' Define enemy plane.
'''


from flying_object import FlyingExplosiveObject


class EnemyPlane(FlyingExplosiveObject):
    '''
    '''

    def __init__(self, background_size, image, explosion_images, size=None):
        ''' Initialize an enemy plane.
        '''

        super().__init__(background_size, image, explosion_images, size)
        self.speed = 5

        self._reset_location()

    def update(self):
        if not self._killed:
            # If alive...
            if self.rect.top < self._background_height:
                self.rect.top += self.speed
            else:
                self._reset_location()
            self._trace_current_location_before_explosion()
        else:
            self._explode()


class FirstTierEnemyPlane(EnemyPlane):

    def __init__(self, background_size, image, explosion_images, size=None):
        super().__init__(background_size, image, explosion_images, size)
