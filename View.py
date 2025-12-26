import math
import random

import numpy
import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo


class Camera:
    def __init__(self):

        self.rotation_x = 0
        self.rotation_y = 0
        self.position_x = 0
        self.position_y = 0
        self.position_z = -2
        self.rotation_speed = 3
        self.move_speed = 0.1
        self.angle=0;

    def apply_transform(self):

        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 5000.0)

        glTranslatef(self.position_x, self.position_y, self.position_z)

        glTranslatef(-self.position_x, -self.position_y, -self.position_z)
        glRotatef(self.rotation_x, 1, 0, 0)  # Вращение вокруг X
        glRotatef(self.rotation_y, 0, 1, 0)  # Вращение вокруг Y
        glTranslatef(self.position_x, self.position_y, self.position_z)

    def handle_keys(self):

        keys = pygame.key.get_pressed()

        # вращение камеры
        if keys[pygame.K_UP]:
            self.rotation_x -= self.rotation_speed
        if keys[pygame.K_DOWN]:
            self.rotation_x += self.rotation_speed
        if keys[pygame.K_LEFT]:
            self.rotation_y -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.rotation_y += self.rotation_speed

        # перемещение камеры
        if keys[pygame.K_w]:
            # движение вперед

            self.position_x += math.sin(-self.rotation_y*math.pi/180)*self.move_speed
            self.position_z += math.cos(-self.rotation_y*(math.pi/180))*self.move_speed
            self.position_y += self.rotation_x*math.pi/180*self.move_speed
        if keys[pygame.K_s]:
            # движение назад
            self.position_x -= math.sin(-self.rotation_y * math.pi / 180) * self.move_speed
            self.position_z -= math.cos(-self.rotation_y * (math.pi / 180)) * self.move_speed
            self.position_y -= self.rotation_x * math.pi / 180 * self.move_speed
        if keys[pygame.K_a]:
            # движение влево
            # self.position_x += self.move_speed
            self.position_x += math.sin(math.pi/2+self.rotation_y * math.pi / 180) * self.move_speed
            self.position_z -= math.cos(math.pi/2+self.rotation_y * (math.pi / 180)) * self.move_speed
        if keys[pygame.K_d]:
            # движение вправо
            self.position_x -= math.sin(math.pi / 2 + self.rotation_y * math.pi / 180) * self.move_speed
            self.position_z += math.cos(math.pi / 2 + self.rotation_y * (math.pi / 180)) * self.move_speed

        # двиежение вверх/вниз
        if keys[pygame.K_q]:
            self.position_y -= self.move_speed
        if keys[pygame.K_e]:
            self.position_y += self.move_speed



# вывод информацию о положении камеры в заголовок окна
def display_camera_info(camera):
    info = f"Camera: Pos({camera.position_x:.1f}, {camera.position_y:.1f}, {camera.position_z:.1f}) Rot({camera.rotation_x:.1f}, {camera.rotation_y:.1f})"
    pygame.display.set_caption(info)


def generate_random_colors_per_vertex(num_vertices):
    """Генерирует случайные цвета для каждой вершины"""
    colors = []
    for _ in range(num_vertices):
        r = random.uniform(0.0, 1.0)
        g = random.uniform(0.0, 1.0)
        b = random.uniform(0.0, 1.0)
        colors.append((r, g, b))

    # Преобразуем в плоский массив float
    flat_colors = []
    for color in colors:
        flat_colors.extend(color)

    return flat_colors


# отрисовка сцены
def show_scene(vertices, normals, colors, light_pos):
    # colors = generate_random_colors_per_vertex(len(vertices))
    vbo_v = vbo.VBO(vertices)
    vbo_n = vbo.VBO(normals)
    vbo_c = vbo.VBO(colors)


    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF | pygame.locals.OPENGL)
    pygame.display.set_caption("Управление камерой")

    glEnable(GL_DEPTH_TEST)

    camera = Camera()
    # light_pos = [-1, 0, 1, 0.0]

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        camera.handle_keys()
        display_camera_info(camera)

        # очистка экрана
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        camera.apply_transform()

        glPointSize(20)
        glBegin(GL_POINTS)
        glVertex3f(-light_pos[0], -light_pos[1], -light_pos[2])
        glEnd()
        # Рисуем сцену

        glEnableClientState(GL_VERTEX_ARRAY)
        # glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        # glEnableClientState(GL_COLOR_ARRAY)

        # полигоны
        vbo_v.bind()
        glVertexPointer(3, GL_FLOAT, 0, vbo_v)
        vbo_v.unbind()

        # # нормали
        # vbo_n.bind()
        # glNormalPointer(GL_FLOAT, 0, vbo_n)
        # vbo_n.unbind()

        vbo_c.bind()
        glColorPointer(3, GL_FLOAT, 0, vbo_c)
        vbo_c.unbind()

        glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        glDisableClientState(GL_COLOR_ARRAY)
        # glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        # Обновляем дисплей
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

