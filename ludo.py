from OpenGL.GL import *
from OpenGL.GLU import *
import pygame

pygame.init()
display_height = 600
display_width = 600
pygame.display.set_mode((display_height, display_width), pygame.OPENGL | pygame.DOUBLEBUF)

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

edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6],
         [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]

faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 4, 7, 3],
         [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6]]

BROWN = (210 / 255, 105 / 255, 30 / 255)


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
    glPushMatrix()
    for face in faces:
        for vertex in face:
            glColor3fv(BROWN)
            glVertex3fv(vertices_table_top[vertex])
    glPopMatrix()
    glEnd()

    glPushMatrix()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices_table_top[vertex])
    glPopMatrix()
    glEnd()


glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()
gluPerspective(45, (display_height / display_width), 0.1, 50)

while True:
    glLoadIdentity()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                glTranslatef(0, -0.5, 0)
            if event.key == pygame.K_a:
                glTranslatef(0.5, 0, 0)
            if event.key == pygame.K_s:
                glTranslatef(0, 0.5, 0)
            if event.key == pygame.K_d:
                glTranslatef(-0.5, 0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                glTranslatef(0, 0, 0.5)
            if event.button == 5:
                glTranslatef(0, 0, -0.5)
    mouse = pygame.mouse.get_rel()

    if pygame.mouse.get_pressed()[2]:
        glRotatef(-0.05 * mouse[0], 0, 0, 0)

    glPushMatrix()
    glLoadIdentity()
    glMultMatrixf(viewMatrix)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    table_leg_1()
    table_leg_2()
    table_leg_3()
    table_leg_4()
    table_top()
    pygame.display.flip()
    pygame.time.wait(10)
