import random
import math
from math import radians, pi, degrees
from ray import Ray
from unit_vector import UnitVector
from angle_range import AngleRange


class RayGenerator:
    def __init__(self):
        self.initial_rays = 5         #or main rays
        self.spotlight_rays = 5
        self.spotlight_range = 10
        self.energy_loss_per_degree = 0.5
       

    def get_initial_sonar_rays(self,sonar_point,range_angle):
        """Initial rays coming out of sonar
            Args::
                sonar_point (:obj:`Point`): sonar center point.
                range_angle (:obj:`AngleRange`): sonar sight range in radians
            Returns:
                :obj:`list` of `Ray`: primary rays
        """
        rays=[]
        for i in range(self.initial_rays):
            angle=range_angle.get_random_angle_in_range()
            ray=Ray(angle,UnitVector(sonar_point,angle),100,0)
            rays.append(ray)
            ray.__str__()
        return rays


    def get_spotlight_rays(self,primary_ray, range_angle):
        """Generates self.spotlight_rays spotlight rays from a primary ray
            Args:
                primary_ray (:obj:`Ray`): ray from which the spotlight rays come out
                range_angle (:obj:`AngleRange`): range in radians to the spotlight rays
            Returns:
                :obj:`list` of `Ray`: spotlight ray for the primary ray
        """
        #Esto va para otro lado, como desde donde llama a esta funcion o una funcion aca, pequennia
        #saca el rango 
        vector = primary_ray.vector
        angle = vector.angle

        max_angle = angle + self.spotlight_range
        min_angle = angle - self.spotlight_range

        min_angle = (360 + min_angle) if (min_angle < 0) else min_angle # adjust negative angle
        max_angle = (max_angle - 360) if (max_angle > 360) else max_angle # adjust over 360 angle
        print("rango para los rayos de foco: ", max_angle,min_angle)
        range_angle = AngleRange(radians(min_angle), radians(max_angle))
        # fin
        point=vector.origin_point
        angles=[]
        rays=[]
        while len(angles) < self.spotlight_rays:
            current_angle = range_angle.get_random_angle_in_range()
            if (angle != current_angle and current_angle not in angles):
                energy = self.get_secondary_ray_energy(primary_ray,current_angle)
                ray=Ray(current_angle,UnitVector(point,current_angle),energy,primary_ray.traveled_distance)
                rays.append(ray)
                angles.append(current_angle)
                ray.__str__()
        return angles


    def get_secondary_rays(self,primary_ray, range_angle):
        """Generates secondary ray in a range_angle, from a primary ray
            Args:
                primary_ray (:obj:`Ray`): ray from which the secondary rays come out
                range_angle (:obj:`AngleRange`): range in radians for secondary angles
            Returns:
                :obj:`list` of `Ray`: secondary rays 
        """
        rays=[]
        for i in range(self.inicial_rays):
            angle=range_angle.get_random_angle_in_range()
            point=primary_ray.vector.origin_point
            energy = self.get_secondary_ray_energy(primary_ray,angle)

            ray=Ray(angle,UnitVector(point,angle),energy,primary_ray.traveled_distance)
            rays.append(ray)
            #ray.__str__()
        return rays


    def get_degrees_difference(self, angle_a, angle_b):
        between_first_and_fourth_quadrant = (angle_a < 90 and angle_b > 270 or angle_b < 90 and angle_a > 270)
        if between_first_and_fourth_quadrant:
            angle_a = (360 - angle_a) if (angle_a > 270) else angle_a # adjust the over 270 angle
            angle_b = (360 - angle_b) if (angle_b > 270) else angle_b
            return angle_a + angle_b
        else:
            return abs(angle_a - angle_b)


    def get_ray_energy_with_loss(self, source_energy, source_degrees, ray_degrees):
        degrees_difference = self.get_degrees_difference(source_degrees, ray_degrees)
        return source_energy - degrees_difference * self.energy_loss_per_degree


    def get_reflected_ray(self, source_ray, line_segment):
        reflection_point = line_segment.get_intersection_point(source_ray.vector)
        reflected_vector = line_segment.get_reflected_vector(reflection_point, source_ray.vector)
        traveled_distance = source_ray.traveled_distance + reflection_point.get_distance_to(source_ray.vector.origin_point)
        bounces = source_ray.bounces + 1

        degrees_from_reflection_point_to_source_ray_origin = degrees(reflected_vector.origin_point.get_angle_to(source_ray.vector.origin_point))
        energy = self.get_ray_energy_with_loss(source_ray.energy, degrees_from_reflection_point_to_source_ray_origin, degrees(reflected_vector.angle))

        reflected_ray = Ray(source_ray.angle_from_sonar, reflected_vector, energy, traveled_distance, bounces)
        return reflected_ray


    def get_secondary_ray_energy(self,primary_ray, angle):
        """Calculate the energy of a secondary ray using the information from a primary ray as a basis
            Args:
                primary_ray (:obj:`Ray`): ray from which the secondary rays get the information
                angle (:obj:`float`): angle in radians for the secondary ray
            Returns:
                int: energy for secondary ray in radians
        """
        angles_degrees_difference = self.get_degrees_difference(degrees(primary_ray.vector.angle), degrees(angle))
        return primary_ray.energy - angles_degrees_difference * self.energy_loss_per_degree
