import pygame
import math
from point import Point
from sonar import Sonar
from line_segment import LineSegment
from vector_utilities import *


screen_width = 500
screen_height = 500
window = pygame.display.set_mode((screen_width, screen_height))
center_point = Point(int(screen_width / 2), int(screen_height / 2))

sonar_line = LineSegment((0,0),(0,0))
sonar = Sonar(center_point)
wall_line_segment = LineSegment(Point(100, 350), Point(400, 350))
sonar_wall_intersection = None

def redraw_window():
    window.fill((5, 5, 5))
    sonar.draw(window)
    sonar_line.draw(window, (255, 255, 255))
    wall_line_segment.draw(window, (63, 193, 201))
    if sonar_wall_intersection:
        sonar_wall_intersection.draw(window, (255, 255, 255), 4)
    pygame.display.update()

run = True
while run:
    mouse_point = Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    sonar.update_rotation(mouse_point)
    sonar_line = LineSegment(center_point, mouse_point)

    redraw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                direction_vector = mouse_point - center_point
                angle = find_angle(center_point, mouse_point) * (180 / math.pi)
                print(angle)
                sonar_wall_intersection = ray_segment_intersection_point(center_point, direction_vector, wall_line_segment.pointB, wall_line_segment.pointA)
                #print(intersection)
