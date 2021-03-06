

class Ray:
    """ Unit vector representation.

        Attributes:
            angle_from_sonar (float): Initial angle from sonar, used to draw an echo pixel.
            energy (float): Ray's sound energy, used to draw an echo pixel.
            traveled_distance (float): Pixels traveled by the ray, used to draw an echo pixel.
            bounces (int): Number of times the ray has bounced.
            vector (:obj:`UnitVector`): Vector that indicates ray origin point and direction.
    """
    def __init__(self, angle_from_sonar, vector, energy=100, traveled_distance=0, bounces=0):
        self.angle_from_sonar = angle_from_sonar # in degrees
        self.energy = energy
        self.traveled_distance = traveled_distance
        self.bounces = bounces
        self.vector = vector


    def __str__(self):
        return 'Ray = ∠{}° E{} {}px {}⭨⭧ {}'.format(int(self.angle_from_sonar), int(self.energy), int(self.traveled_distance), self.bounces, str(self.vector))


    def __repr__(self):
        return self.__str__()
