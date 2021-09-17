from pygame.math import Vector2
import pygame as pg

all_points = []
target_point = None

# Parameters
default_controls_lock_state = True

point_color = (204, 255, 255)
line_color = (255, 255, 255)
controller_point_color = (127, 127, 127)
controller_line_color = (200, 200, 200)

point_radius = 4
controller_point_radius = 2

line_width = 2
controller_line_width = 1

searching_radius = 50


class Point:
    def __init__(self, coordinates):
        self.position = Vector2(coordinates)

        self.a_controller = self.position + Vector2(0, 40)  # first turn
        self.b_controller = self.position + Vector2(0, -40)  # second turn

        all_points.append(self)

    def draw_point(self, surface):
        pg.draw.circle(surface, point_color, self.position, point_radius)

    def draw_controllers(self, surface):
        pg.draw.line(surface, controller_line_color, self.position, self.a_controller, controller_line_width)
        pg.draw.circle(surface, controller_point_color, self.a_controller, controller_point_radius)
        pg.draw.line(surface, controller_line_color, self.position, self.b_controller, controller_line_width)
        pg.draw.circle(surface, controller_point_color, self.b_controller, controller_point_radius)

    def update(self, pos, label):
        if label == 'c':
            self.a_controller = Vector2(pos) + (self.a_controller - self.position)
            self.b_controller = Vector2(pos) + (self.b_controller - self.position)
            self.position.update(pos)
        elif label == 'a':
            self.a_controller = Vector2(pos)
            self.b_controller = 2 * self.position - self.a_controller
        elif label == 'b':
            self.b_controller = Vector2(pos)
            self.a_controller = 2 * self.position - self.b_controller


def get_point(p0: Point, p1: Point, t):
    return p0.position*(-t*t*t + 3*t*t - 3*t + 1) + \
           p0.b_controller*(3*t*t*t - 6*t*t + 3*t) + \
           p1.a_controller*(-3*t*t*t + 3*t*t) + \
           p1.position*t*t*t


def draw_cubic_curve(surface, a: Point, b: Point, dt):
    point1 = get_point(a, b, 0)
    for i in range(1, int(1 / dt) + 1):
        point2 = get_point(a, b, i * dt)
        pg.draw.line(surface, line_color, point1, point2, line_width)
        point1 = point2


def draw_curves(surface, dt):
    n = len(all_points)
    if n > 1:
        for i in range(n-1):
            draw_cubic_curve(surface, all_points[i], all_points[i+1], dt)
    elif n == 1:
        pg.draw.circle(surface, line_color, all_points[0].position, max(line_width // 2, 1))


def nearest_point_within_radius(pos, radius):
    min_dist = radius
    min_point = None
    for point in all_points:
        dist = point.position.distance_to(pos)
        if dist <= radius and dist <= min_dist:
            min_dist = dist
            min_point = point
    return min_point


def get_target_point(pos, pressed):
    global target_point

    if not target_point:
        target_point = nearest_point_within_radius(pos, searching_radius)
    elif not pressed:
        r = (target_point.a_controller - target_point.b_controller).length()
        if not(target_point.position.distance_to(pos) < r
                or target_point.a_controller.distance_to(pos) < r
                or target_point.b_controller.distance_to(pos) < r):
            target_point = None
    return target_point


