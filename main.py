import pygame
from point import Point
from sonar import Sonar
from line_segment import LineSegment
from unit_vector import UnitVector

screen_width = 500
screen_height = 500
window = pygame.display.set_mode((screen_width, screen_height))
center_point = Point(int(screen_width / 2), int(screen_height / 2))

sonar_line = LineSegment((0,0),(0,0))
sonar = Sonar(center_point)

line_segments = [LineSegment(Point(100, 50), Point(400, 50)), LineSegment(Point(100, 450), Point(400, 450)), LineSegment(Point(50, 100), Point(50, 400)), LineSegment(Point(450, 100), Point(450, 400))]
reflected_vectors = [None] * 4

def redraw_window():
    window.fill((5, 5, 5))
    sonar.draw(window)
    sonar_line.draw(window, (255, 255, 255))

    for line in line_segments:
        line.draw(window, (255, 255, 255))

    for vector in reflected_vectors:
        if vector is not None:
            vector.draw(window, 30, (255, 51, 153))
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
                ray_vector = UnitVector(center_point, center_point.get_angle_to(mouse_point))
                for index, line_segment in enumerate(line_segments):
                    reflection_point = line_segment.intersects(ray_vector)
                    if reflection_point is not None:
                        v= line_segment.get_reflected_vector(reflection_point, ray_vector)
                        reflected_vectors[index] =v
                        sonar.sonar_collision(v)


