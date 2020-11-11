import pygame
from math import radians, degrees
from point import Point
from sonar import Sonar
from line_segment import LineSegment
from unit_vector import UnitVector
from ray_generator import RayGenerator
from ray import Ray
from echo_pixel import EchoPixel
import threading


def generate_echo_pixels(source_ray, sonar, line_obstacles, echo_pixels):
    """Recursive function that generates the echo pixels for a shot source ray.

        Args:
            source_ray (:obj:`Ray`): Source ray to check collisions.
            sonar (:obj:`Sonar`): Game only sonar.
            line_obstacles (:obj:`list` of :obj:`Sonar`): List of displayed line obstacles.
            echo_pixels (:obj:`list` of :obj:`EchoPixel`): List of displayed echo pixels.
    """
    if source_ray.bounces >= 2 or source_ray.energy <= 10:
        return

    if sonar.collides(source_ray.vector):
        source_ray.traveled_distance += sonar.center_point.get_distance_to(source_ray.vector.origin_point) # update traveled distance for collision
        pixel_energy = RayGenerator.get_energy_with_distance_loss(source_ray.energy, source_ray.traveled_distance)
        if pixel_energy > 0:
            pixel_x, pixel_y = sonar.get_coordinates_around_center(radians(source_ray.angle_from_sonar), int(source_ray.traveled_distance/2))
            generated_echo_pixel = EchoPixel(pixel_energy, Point(pixel_x, pixel_y))
            echo_pixels.append(generated_echo_pixel) # add pixel to drawing list
        return

    hit_line = LineSegment.get_nearest_intersected_line(source_ray.vector, line_obstacles)
    ray_bounced = (hit_line is not None)
    if ray_bounced:
        reflected_ray = RayGenerator.get_reflected_ray(source_ray, hit_line)
        if reflected_ray.energy > 0:
            returning_ray = RayGenerator.get_returning_reflected_ray(reflected_ray, source_ray)
            generated_rays = [reflected_ray, returning_ray]

            reflection_angle_range = hit_line.get_reflection_angle_range(reflected_ray.vector.origin_point, source_ray.vector)

            secondary_rays = RayGenerator.get_secondary_rays(reflected_ray, reflection_angle_range)
            generated_rays.extend(secondary_rays)

            spotlight_rays = []
            for ray in generated_rays:
                spotlight_rays.extend(RayGenerator.get_spotlight_rays(ray))
            generated_rays.extend(spotlight_rays)

            for ray in generated_rays:
                generate_echo_pixels(ray, sonar, line_obstacles, echo_pixels)


def shoot_sonar_rays(mouse_point, sonar, line_obstacles, echo_pixels):
    """Shoots all the initial rays from the sonar.

        Args:
            mouse_point (:obj:`Point`): Point of the mouse cursor.
            sonar (:obj:`Sonar`): Game only sonar.
            line_obstacles (:obj:`list` of :obj:`Sonar`): List of displayed line obstacles.
            echo_pixels (:obj:`list` of :obj:`EchoPixel`): List of displayed echo pixels.
    """
    sonar_ray_vector = UnitVector(sonar.center_point, sonar.center_point.get_angle_to(mouse_point))
    main_ray = Ray(degrees(sonar_ray_vector.angle), sonar_ray_vector)

    sonar_view_range = sonar.get_view_angle_range()
    initial_sonar_rays = RayGenerator.get_initial_sonar_rays(sonar.center_point, sonar_view_range)
    initial_sonar_rays.append(main_ray)

    spotlight_rays = []
    for ray in initial_sonar_rays:
        spotlight_rays.extend(RayGenerator.get_spotlight_rays(ray))
    initial_sonar_rays.extend(spotlight_rays)#"""

    angle_threads = []
    for ray in initial_sonar_rays:
        thread = threading.Thread(target=generate_echo_pixels, args=[ray, sonar, line_obstacles, echo_pixels])
        angle_threads.append(thread)
        thread.start()

    for thread in angle_threads:
        thread.join()


def redraw_window(window, sonar, line_obstacles, echo_pixels):
    """Redraws all the sprites in screen.

        Args:
            window (:obj:`Surface`:): Pygame window surface.
            sonar (:obj:`Sonar`): Game only sonar.
            line_obstacles (:obj:`list` of :obj:`Sonar`): List of displayed line obstacles.
            echo_pixels (:obj:`list` of :obj:`EchoPixel`): List of displayed echo pixels.
    """
    window.fill((0, 0, 0)) # black background
    sonar.draw(window)

    for line in line_obstacles:
        line.draw(window)

    for echo_pixel in echo_pixels:
        echo_pixel.draw(window)
    pygame.display.update()


def run_main():
    """Runs the pygame loop of the simulation.
    """
    screen_width = screen_height = 700
    window = pygame.display.set_mode((screen_width, screen_height))
    center_point = Point(int(screen_width / 2), int(screen_height / 2))

    sonar = Sonar(center_point) # sonar that shoot sound waves
    echo_pixels = [] # list of displayed echo pixels

    map_1 = [LineSegment(Point(250, 250), Point(450, 250), 0.4), LineSegment(Point(250, 450), Point(450, 450)), LineSegment(Point(250, 250), Point(250, 450), 0.8), LineSegment(Point(450, 250), Point(450, 450))]
    map_2 = [LineSegment(Point(210, 400), Point(210, 450), 1),LineSegment(Point(210, 250), Point(210, 300)),LineSegment(Point(500, 400), Point(500, 450),0.7),LineSegment(Point(500, 300),Point(500, 345)),LineSegment(Point(600, 200), Point(600, 500), 1),LineSegment(Point(100, 100), Point(600, 100)),LineSegment(Point(100, 600), Point(340, 600)), LineSegment(Point(300, 500), Point(300, 600))]
    map_3 = [LineSegment(Point(150, 200), Point(150, 500),0.2), LineSegment(Point(400, 250), Point(400, 400)), LineSegment(Point(350, 400), Point(450, 400)), LineSegment(Point(250, 550), Point(345, 550),1), LineSegment(Point(100, 550), Point(200, 550)), LineSegment(Point(100, 150), Point(400, 150),0.2), LineSegment(Point(420, 150), Point(420, 200),1)]
    maps = [map_1, map_2, map_3] # all maps available
    map_number = 1 # used to change map
    line_obstacles = maps[map_number]

    wave_threads = []
    run = True
    while run:
        mouse_point = Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        sonar.update_rotation(mouse_point)
        redraw_window(window, sonar, line_obstacles, echo_pixels)

        dead_threads_indexes = []  # join/kill inactive wave threads
        for index, thread in enumerate(wave_threads):
            if not thread.is_alive():
                thread.join()
                dead_threads_indexes.insert(0, index)
        for dead_thread_index in dead_threads_indexes:
            wave_threads.pop(dead_thread_index)
        for t in wave_threads: # print active wave threads
            print("T", end='')
        print("")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            set_next_map = (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)
            if set_next_map: # space bar key
                next_map_number = map_number + 1
                map_number = 0 if (next_map_number >= len(maps)) else next_map_number
                line_obstacles = maps[map_number]
                echo_pixels = []

            reset_echo_pixels = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3)
            if reset_echo_pixels: # right mouse click
                echo_pixels = []

            shoot_sound_rays = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            if shoot_sound_rays: # left mouse click
                wave_thread = threading.Thread(target=shoot_sonar_rays, args=[mouse_point, sonar, line_obstacles, echo_pixels])
                wave_thread.start()
                wave_threads.append(wave_thread)


if __name__ == "__main__":
    run_main()