import pygame as pg
from pygame.math import Vector2
from point import Point, nearest_point_within_radius, draw_curves, point_radius, get_target_point

WIDTH, HEIGHT = 720, 560
FPS = 60

pg.init()
main_screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Bezier Curves')

clock = pg.time.Clock()

dt = 0.01
grab_radius = 6

pressed = False
target_label = None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pressed = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                pressed = False
                target_label = None

    main_screen.fill('black')

    pos = pg.mouse.get_pos()

    nearest_point = get_target_point(pos, pressed)
    if nearest_point:
        nearest_point.draw_point(main_screen)
        nearest_point.draw_controllers(main_screen)

    if pressed:
        if nearest_point:
            if not target_label:
                if nearest_point.position.distance_to(pos) < grab_radius:
                    target_label = 'c'
                elif nearest_point.a_controller.distance_to(pos) < grab_radius:
                    target_label = 'a'
                elif nearest_point.b_controller.distance_to(pos) < grab_radius:
                    target_label = 'b'
            nearest_point.update(pos, target_label)
        else:
            Point(pos)

    draw_curves(main_screen, dt)

    pg.display.update()
    clock.tick(FPS)
