import pygame


class EchoPixel:
    """ Pixel that represents an echo of sound.

        Attributes:
            display_point (:obj:`Point`): Point to display the pixel.
            display_pixel (:obj:`Surface`:): Pygame surface of the pixel with transparency.
    """
    def __init__(self, energy, display_point, size=5):
        self.display_point = display_point
        self.display_pixel = pygame.Surface((size, size))

        transparency = int((energy/100) * 255)
        self.display_pixel.set_alpha(transparency)
        self.display_pixel.fill((255, 255, 255)) # white

    def draw(self, window):
        """ Draws the echo pixel in the pygame game window.

            Args:
                window(:obj:`Surface`:): Pygame window surface.
        """
        window.blit(self.display_pixel, self.display_point.get_int_tuple())
