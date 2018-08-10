''' Define customized groups.
'''


import pygame


class ExplosionGroup(pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

    def restore_location_before_explosion(self):
        for sp in self:
            sp.restore_location_before_explosion()


class LaserGroup(pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

    def kill_hitted_lasers(self):
        for hit in self:
            if hit.is_hitted():
                hit.kill()
