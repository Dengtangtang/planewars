''' Base class.
'''

import pygame


class FlyingObject(pygame.sprite.Sprite):
    '''
    '''

    def _reset_location(self):
        raise NotImplementedError('define specific _reset_location')

    def __init__(self, background_size, image, size=None):
        '''
        '''

        super().__init__()
        self.image = image
        if size is not None:
            self.image = pygame.transform.smoothscale(self.image, size)

        self.rect = self.image.get_rect()
        self._origin_image = self.image

        self._background_width = background_size[0]
        self._background_height = background_size[1]

        # Attributes may/shall be overwritten for each flying object.
        self._speed = 5


class FlyingExplosiveObject(FlyingObject):
    '''
    '''

    def _reset_location(self):
        raise NotImplementedError('define specific _reset_location')

    def _reset_after_explosion(self):
        self._killed = False
        self.image = self._origin_image
        self._blood = self._origin_blood
        self._hit_damage = self._origin_hit_damage
        self._reset_location()

    def _trace_current_location_before_explosion(self):
        self._curr_rect_left = self.rect.left
        self._curr_rect_top = self.rect.top

    def _explode(self):
        if 0 <= self._explosion_counter < len(self._explosions):
            # Update image...
            explo = self._explosions[self._explosion_counter]
            self.image = explo

            # Update location (move to center)...
            explo_rect = explo.get_rect()
            explo_rect.center = self.rect.center
            self.rect.left = explo_rect.left
            self.rect.top = explo_rect.top

            # Update counter...
            self._explosion_counter += 1
        else:
            self._explosion_counter = 0

        # Set hit damage to zero when explosion, or the explosion will hurt the plane.
        self._hit_damage = 0

    def __init__(self, background_size, image, explosion_images, blood, hit_damage, size=None):
        super().__init__(background_size, image, size)
        self._explosions = explosion_images
        self._explosion_counter = 0
        self._curr_rect_left = self.rect.left
        self._curr_rect_top = self.rect.top
        self._killed = False
        self._blood = blood
        self._origin_blood = self._blood
        self._hit_damage = hit_damage
        self._origin_hit_damage = self._hit_damage

    def is_killed(self):
        return self._killed

    def set_killed(self, v=True):
        self._killed = v

    def restore_location_before_explosion(self):
        ''' Restore self.rect's location to when the object is alive.
        '''

        self.rect.left = self._curr_rect_left
        self.rect.top = self._curr_rect_top
        if self._explosion_counter == 0 and self._killed:
            self._reset_after_explosion()

    def lose_blood(self, damage):
        self._blood -= damage

    def get_hit_damage_value(self):
        return self._hit_damage

    def get_blood(self):
        return self._blood
