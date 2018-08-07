''' Define player plane.
'''


import pygame


class PlayerPlane(pygame.sprite.Sprite):
    '''
    '''

    def __init__(self, image, background_size):
        ''' Initialize a player plane.
        '''

        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()  # Load image.
        self.rect = self.image.get_rect()  # Get 'Rect' object (position).
        self._background_width, self._background_height = background_size[0], background_size[1]
        self.speed = 10

        # Initialize position.
        self.rect.left = (self._background_width - self.rect.width) // 2
        self.rect.top = self._background_height - self.rect.height

    def move_left(self):
        ''' Move the plane left.
        '''

        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        ''' Move the plane right.
        '''

        if self.rect.right < self._background_width:
            self.rect.left += self.speed
        else:
            self.rect.left = self._background_width - self.rect.width

    def move_up(self):
        ''' Move the plane up.
        '''

        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        ''' Move the plane down.
        '''

        if self.rect.bottom < self._background_height:
            self.rect.top += self.speed
        else:
            self.rect.top = self._background_height - self.rect.height
