from pygame.sprite import Group


class ContainerGroup(Group):

    def __init__(self, screen_size, *sprites):
        super().__init__(*sprites)
        self._screen_width = screen_size[0]
        self._screen_height = screen_size[1]
        # self._sprites = []

    # def kill_all(self):
    #     for sprite in self:
    #         if sprite.rect.top >= self._screen_height or sprite.is_killed():
    #             sprite.kill()
