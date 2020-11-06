from math import degrees

class Ray:
    def __init__(self, angle_from_sonar, vector, energy=100, traveled_distance=0, bounces=0):
        self.angle_from_sonar = angle_from_sonar
        self.energy = energy
        self.traveled_distance = traveled_distance
        self.vector = vector
        self.bounces = bounces


    def __str__(self):
        return 'Ray = ∠{}, E{}, {}px, {} bounces, {}'.format(int(self.angle_from_sonar), int(self.energy), int(self.traveled_distance), self.bounces, str(self.vector))


    def __repr__(self):
        return self.__str__()
