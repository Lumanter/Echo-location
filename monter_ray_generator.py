import random
import math
from math import radians, pi, degrees
from ray import Ray
from unit_vector import UnitVector
from angle_range import AngleRange


class MonterRayGenerator:
    def __init__(self):
        self.inicial_rays = 5         #or main rays
        self.spotlight_rays = 5
        self.spotlight_range = 10
       
    def get_initial_sonar_rays(self,sonar_point,range_angle):
        """Initial rays coming out of sonar
            Attributes:
                angle_angle (AngleRange): range for angles, in radians.
        """
        rays=[]
        for i in range(self.inicial_rays):
            angle=math.degrees(range_angle.get_random_angle_in_range())
            ray=Ray(angle,UnitVector(sonar_point,angle),100,0)
            rays.append(ray)
            ray.__str__()
        return rays
    def get_spotlight_rays(self,primary_ray, range_angle):
        """
        genera los rayos que hacen de foco
        """
        vector = primary_ray.vector
        angle = vector.angle

        max_angle = angle + self.spotlight_range
        min_angle = angle - self.spotlight_range

        min_angle = (360 + min_angle) if (min_angle < 0) else min_angle # adjust negative angle
        max_angle = (max_angle - 360) if (max_angle > 360) else max_angle # adjust over 360 angle
        print("rango para los rayos de foco: ", max_angle,min_angle)
        range_angle = AngleRange(radians(min_angle), radians(max_angle))

        point=vector.origin_point
        angles=[]
        while len(angles) < self.spotlight_rays:
            current_angle=math.degrees(range_angle.get_random_angle_in_range())
            if (angle != current_angle and current_angle not in angles):
                energy = self.get_secondary_ray_energy(primary_ray,current_angle)
                ray=Ray(current_angle,UnitVector(point,current_angle),energy,primary_ray.traveled_distance)
                angles.append(ray)
                ray.__str__()
        return angles
    def get_secondary_rays(self,primary_ray, range_angle):
        rays=[]
        for i in range(self.inicial_rays):
            angle=math.degrees(range_angle.get_random_angle_in_range())
            point=primary_ray.vector.origin_point
            energy = self.get_secondary_ray_energy(primary_ray,angle)

            ray=Ray(angle,UnitVector(point,angle),energy,primary_ray.traveled_distance)
            rays.append(ray)
            #ray.__str__()
        return rays
    def get_secondary_ray_energy(self,primary_ray, angle):
        return primary_ray.energy - 30
