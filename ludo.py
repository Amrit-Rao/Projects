from math import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import pygame

pygame.init()
display_height = 600
display_width = 600
pygame.display.set_mode((display_height, display_width), pygame.OPENGL | pygame.DOUBLEBUF)

vertices_ground = [[-50, -50, -2.5], [50, -50, -2.5], [50, 50, -2.5], [-50, 50, -2.5]]

vertices_table_leg_1 = [[-2, -2, -2.5], [-1, -2, -2.5], [-1, -1, -2.5], [-2, -1, -2.5],
                        [-2, -2, 1.5], [-1, -2, 1.5], [-1, -1, 1.5], [-2, -1, 1.5]]
vertices_table_leg_2 = [[-2, 1, -2.5], [-1, 1, -2.5], [-1, 2, -2.5], [-2, 2, -2.5],
                        [-2, 1, 1.5], [-1, 1, 1.5], [-1, 2, 1.5], [-2, 2, 1.5]]
vertices_table_leg_3 = [[1, -2, -2.5], [2, -2, -2.5], [2, -1, -2.5], [1, -1, -2.5],
                        [1, -2, 1.5], [2, -2, 1.5], [2, -1, 1.5], [1, -1, 1.5]]
vertices_table_leg_4 = [[1, 1, -2.5], [2, 1, -2.5], [2, 2, -2.5], [1, 2, -2.5],
                        [1, 1, 1.5], [2, 1, 1.5], [2, 2, 1.5], [1, 2, 1.5]]

vertices_table_top = [[-2, -2, 1.5], [2, -2, 1.5], [2, 2, 1.5], [-2, 2, 1.5],
                      [-2, -2, 2.5], [2, -2, 2.5], [2, 2, 2.5], [-2, 2, 2.5]]

vertices_dice = np.array([[-0.05, - 0.05, 2.5], [0.05, - 0.05, 2.5], [0.05, 0.05, 2.5], [-0.05, 0.05, 2.5],
                          [-0.05, - 0.05, 2.6], [0.05, - 0.05, 2.6], [0.05, 0.05, 2.6], [-0.05, 0.05, 2.6]])

edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
         [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]

edges_ground = [[0, 1], [1, 2], [2, 3], [3, 0]]

faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 4, 7, 3],
         [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6]]

faces_ground = [[0, 1, 2, 3]]

DICE_SIZE = 0.1
GREEN = (0, 1, 0)
BROWN = (105 / 255, 51 / 255, 15 / 255)
WHITE = (1, 1, 1)
PI = 3.1415

dice_flip_x = 0
dice_flip_y = 0
z_threshold = 100
z_threshold_hit = True
dice_rotate_1 = 0
dice_rotate_2 = 0
dice_rotate_3 = 0
theta = 0
psi = 30
x = 0
y = 0
z = 2.5 + DICE_SIZE / 2
u_x = 0
u_y = 0
u_z = 0
diagonal = 0


def direction_cosines(x1, y1, z1, x2, y2, z2):
    r = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2) + pow((z2 - z1), 2))
    return (x2 - x1) / r, (y2 - y1) / r, (z2 - z1) / r


def new_x_translation(old_x, shift):
    new_x_coordinate = old_x + shift
    return new_x_coordinate


def new_y_translation(old_y, shift):
    new_y_coordinate = old_y + shift
    return new_y_coordinate


def new_z_translation(old_z, shift):
    new_z_coordinate = old_z + shift
    return new_z_coordinate


def new_x_rotation(old_x, old_y, old_z, angle):
    global u_x, u_y, u_z
    new_x_coordinate = old_x * (cos(degree(angle)) + pow(u_x, 2) * (1 - cos(degree(angle)))) + old_y * (
            u_x * u_y * (1 - cos(degree(angle))) - u_z * sin(degree(angle))) + old_z * (
                               u_x * u_z * (1 - cos(degree(angle))) + u_y * sin(degree(angle)))
    return new_x_coordinate


def new_y_rotation(old_x, old_y, old_z, angle):
    global u_x, u_y, u_z
    new_y_coordinate = old_x * (u_y * u_x * (1 - cos(degree(angle))) + u_z * sin(degree(angle))) + old_y * (
            cos(degree(angle)) + pow(u_y, 2) * (1 - cos(degree(angle)))) + old_z * (
                               u_y * u_z * (1 - cos(degree(angle))) - u_x * sin(degree(angle)))
    return new_y_coordinate


def new_z_rotation(old_x, old_y, old_z, angle):
    global u_x, u_y, u_z
    new_z_coordinate = old_x * (u_z * u_x * (1 - cos(degree(angle))) - u_y * sin(degree(angle))) + old_y * (
            u_z * u_y * (1 - cos(degree(angle))) + u_x * sin(degree(angle))) + old_z * (
                               cos(degree(angle)) + pow(u_z, 2) * (1 - cos(degree(angle))))
    return new_z_coordinate


def table_leg_1():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(BROWN)
            glVertex3fv(vertices_table_leg_1[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_table_leg_1[vertex])
    glEnd()


def table_leg_2():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(BROWN)
            glVertex3fv(vertices_table_leg_2[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_table_leg_2[vertex])
    glEnd()


def table_leg_3():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(BROWN)
            glVertex3fv(vertices_table_leg_3[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_table_leg_3[vertex])
    glEnd()


def table_leg_4():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(BROWN)
            glVertex3fv(vertices_table_leg_4[vertex])
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_table_leg_4[vertex])
    glEnd()


def table_top():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(BROWN)
            glVertex3fv(vertices_table_top[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_table_top[vertex])
    glEnd()


def ground():
    glBegin(GL_QUADS)
    for face in faces_ground:
        for vertex in face:
            glColor3fv(GREEN)
            glVertex3fv(vertices_ground[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges_ground:
        for vertex in edge:
            glVertex3fv(vertices_ground[vertex])
    glEnd()


def dice():
    global vertices_dice
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv(WHITE)
            glVertex3fv(vertices_dice[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_dice[vertex])
    glEnd()


def randomize():
    global z_threshold, z_threshold_hit, dice_flip_y, dice_flip_x, dice_rotate_1, dice_rotate_2, dice_rotate_3
    dice_flip_y = np.random.randint(10)
    dice_flip_x = np.random.randint(10)
    z_threshold = np.random.randint(4, 7)
    dice_rotate_1 = 0
    dice_rotate_2 = 0
    dice_rotate_3 = 0
    z_threshold_hit = False


def rotate(x1, y1, z1, x2, y2, z2, angle):
    global vertices_dice, u_x, u_y, u_z
    u_x, u_y, u_z = direction_cosines(x1, y1, z1, x2, y2, z2)
    for i in range(8):
        old_x = new_x_translation(vertices_dice[i][0], -x1)
        old_y = new_x_translation(vertices_dice[i][1], -y1)
        old_z = new_x_translation(vertices_dice[i][2], -z1)

        new_x = new_x_translation(new_x_rotation(old_x, old_y, old_z, angle), x1)
        new_y = new_y_translation(new_y_rotation(old_x, old_y, old_z, angle), y1)
        new_z = new_z_translation(new_z_rotation(old_x, old_y, old_z, angle), z1)

        vertices_dice[i][0] = new_x
        vertices_dice[i][1] = new_y
        vertices_dice[i][2] = new_z


def gravity():
    global vertices_dice, x, y, z, z_threshold_hit, z_threshold, dice_rotate_1, \
        dice_rotate_2, dice_rotate_3, u_x, u_y, u_z, diagonal

    if z >= z_threshold:
        z_threshold_hit = True

    if z_threshold_hit:
        if z > 2.5 + DICE_SIZE / 2:
            z -= 0.05
            for i in range(8):
                vertices_dice[i][2] -= 0.05
    else:
        z += 0.05
        for i in range(8):
            vertices_dice[i][2] += 0.05

    touching_vertices = vertices_dice[np.where(vertices_dice[:, 2] <= 2.5)]

    if touching_vertices.size / 3 == 1:
        offset = 0
        for i in range(8):
            if vertices_dice[i][2] < 2.5:
                offset = 2.5 - vertices_dice[i][2]
                diagonal = get_diagonal(i)
                break
        for i in range(8):
            z += offset
            vertices_dice[i][2] += offset

        rotate(touching_vertices[0][0], touching_vertices[0][1], touching_vertices[0][2],
               vertices_dice[diagonal][0], vertices_dice[diagonal][1],
               vertices_dice[diagonal][2], dice_rotate_1)
        dice_rotate_1 += 0.1

    elif touching_vertices.size / 3 == 2:
        for i in range(8):
            if vertices_dice[i][2] < 2.5:
                offset = (2.5 - vertices_dice[i][2])
                angle = asin(offset / DICE_SIZE)
                z += offset
                diagonal = get_diagonal(i)
                rotate(vertices_dice[i][0], vertices_dice[i][1], vertices_dice[i][2],
                       vertices_dice[diagonal][0], vertices_dice[diagonal][1], vertices_dice[diagonal][2], -angle)
                break

        rotate(touching_vertices[0][0], touching_vertices[0][1], touching_vertices[0][2],
               touching_vertices[1][0], touching_vertices[1][1], touching_vertices[1][2], dice_rotate_2)

        dice_rotate_2 += 0.1

    elif touching_vertices.size / 3 == 0:
        rotate(x, y, z, dice_flip_x, dice_flip_y, 0, dice_rotate_3)
        dice_rotate_3 += 0.1


def degree(radian):
    return radian * pi / 180


def get_diagonal(vertex):
    if vertex == 0 or vertex == 1 or vertex == 4 or vertex == 5:
        return vertex + 2
    else:
        return vertex - 2


glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display_width / display_height), 0.1, 50.0)

glTranslatef(0, 0, -10)
glRotatef(-30, 1, 0, 0)

while True:
    mouse = pygame.mouse.get_rel()
    keyboard = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[2]:
        glRotatef(mouse[0] * 0.1, 0, 0, 1)
        glRotatef(mouse[1] * 0.1, -1 * cos(degree(theta)), sin(degree(theta)), 0)
        theta += mouse[0] * 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                glTranslatef(-sin(degree(theta)) * sin(degree(psi)), - cos(degree(theta)) * sin(degree(psi)),
                             cos(degree(psi)))
            if event.button == 5:
                glTranslatef(sin(degree(theta)) * sin(degree(psi)), cos(degree(theta)) * sin(degree(psi)),
                             - cos(degree(psi)))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                randomize()
    if keyboard[pygame.K_w]:
        glTranslatef(-sin(degree(theta)) / 10, -cos(degree(theta)) / 10, 0)
    if keyboard[pygame.K_a]:
        glTranslatef(cos(degree(theta)) / 10, -sin(degree(theta)) / 10, 0)
    if keyboard[pygame.K_s]:
        glTranslatef(sin(degree(theta)) / 10, cos(degree(theta)) / 10, 0)
    if keyboard[pygame.K_d]:
        glTranslatef(-cos(degree(theta)) / 10, sin(degree(theta)) / 10, 0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    ground()

    glPushMatrix()
    table_leg_1()
    table_leg_2()
    table_leg_3()
    table_leg_4()
    table_top()
    glPopMatrix()

    glPushMatrix()
    gravity()
    dice()
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
