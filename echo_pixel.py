import pygame


class EchoPixel:
    """ Pixel that represents an echo of sound.

        Attributes:
            display_point (:obj:`Point`): Point to display the pixel.
            display_pixel (:obj:`Surface`:): Pygame surface of the pixel with transparency.
    """
    def __init__(self, energy, display_point):
        self.display_point = display_point
        size = 5
        self.display_pixel = pygame.Surface((size, size))

        transparency = int((energy/100) * 255)
        #print("E", energy, ", transparency: ", transparency)
        self.display_pixel.set_alpha(transparency)

        color_white = (255, 255, 255)
        self.display_pixel.fill(color_white)


    """ Draws the echo pixel in the pygame game window.

        Args:
            window(:obj:`Surface`:): Pygame window surface.
    """
    def draw(self, window):
        window.blit(self.display_pixel, self.display_point.get_int_tuple())
