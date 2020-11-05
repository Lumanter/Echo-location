class Ray:
    def __init__(self, angle_from_sonar, vector, energy=100, traveled_distance=0, bounces=0):
        self.angle_from_sonar = angle_from_sonar
        self.energy = energy
        self.traveled_distance = traveled_distance
        self.vector = vector
        self.bounces = bounces

    def __str__(self):
        print("angle from sonar: ",self.angle_from_sonar," energy: ",self.energy,"traveled distance: ",self.traveled_distance,"")
