from math import radians, degrees
import random


class AngleRange:
    """ Range of math angles in radians. Angles are in the [0, 2π] values.

        Attributes:
            min (float): Minimum angle in the range, in radians.
            max (float): Maximum angle in the range, in radians.
    """
    def __init__(self, min, max):
        self.min = min
        self.max = max


    def contains(self, angle):
        """ Indicates if an angle is contained in the angle range.

            Args:
                angle (float): Board object instance with the current game state.

            Returns:
                bool: True if angle is contained, false otherwise.
        """
        if self.min > self.max: # range goes from higher to lower angle
            return angle <= self.max or angle >= self.min
        else:
            return self.min <= angle <= self.max


    def get_random_angle_in_range(self):
        """ Returns a random angle within the range.

            Returns:
                float: Random angle in radians.
        """
        min_degrees, max_degrees = int(degrees(self.min)), int(degrees(self.max))
        if self.min > self.max: # range goes from higher to lower angle
            random_degrees = random.randint(min_degrees, min_degrees + max_degrees)
            random_degrees = (random_degrees - 360) if (random_degrees > 360) else random_degrees # adjust angle to [0, 360]
            return radians(random_degrees)
        else:
            return radians(random.randint(min_degrees, max_degrees))


    def __str__(self):
        return '[{}°, {}°]'.format(int(degrees(self.min)), int(degrees(self.max)))
