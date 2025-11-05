import time

import numpy as np
import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo
from read_file import ReadFile


class Camera:
    def __init__(self):
        self.rotation_x = 0  # Вращение вокруг оси X
        self.rotation_y = 0  # Вращение вокруг оси Y
        self.position_x = 0  # Позиция камеры по X
        self.position_y = 0  # Позиция камеры по Y
        self.position_z = -8  # Позиция камеры по Z
        self.rotation_speed = 3  # Скорость вращения
        self.move_speed = 0.1  # Скорость перемещения

    def apply_transform(self):
        """Применяет трансформации камеры"""
        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 5000.0)

        # Сначала перемещаем камеру, потом вращаем
        glTranslatef(self.position_x, self.position_y, self.position_z)
        glRotatef(self.rotation_x, 1, 0, 0)  # Вращение вокруг X
        glRotatef(self.rotation_y, 0, 1, 0)  # Вращение вокруг Y

    def handle_keys(self):
        """Обрабатывает нажатия клавиш"""
        keys = pygame.key.get_pressed()

        # ВРАЩЕНИЕ КАМЕРЫ - Стрелки
        if keys[pygame.K_UP]:
            self.rotation_x -= self.rotation_speed
        if keys[pygame.K_DOWN]:
            self.rotation_x += self.rotation_speed
        if keys[pygame.K_LEFT]:
            self.rotation_y -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.rotation_y += self.rotation_speed

        # ПЕРЕМЕЩЕНИЕ КАМЕРЫ - WASD
        if keys[pygame.K_w]:
            # Двигаемся вперед (по оси Z)
            self.position_z += self.move_speed
        if keys[pygame.K_s]:
            # Двигаемся назад (по оси Z)
            self.position_z -= self.move_speed
        if keys[pygame.K_a]:
            # Двигаемся влево (по оси X)
            self.position_x += self.move_speed
        if keys[pygame.K_d]:
            # Двигаемся вправо (по оси X)
            self.position_x -= self.move_speed

        # ПЕРЕМЕЩЕНИЕ ВВЕРХ/ВНИЗ - Q/E
        if keys[pygame.K_q]:
            # Двигаемся вверх (по оси Y)
            self.position_y -= self.move_speed
        if keys[pygame.K_e]:
            # Двигаемся вниз (по оси Y)
            self.position_y += self.move_speed

        # ПРИБЛИЖЕНИЕ/ОТДАЛЕНИЕ - +/-
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            self.position_z += 0.5
        if keys[pygame.K_MINUS]:
            self.position_z -= 0.5

        # СБРОС КАМЕРЫ - R
        if keys[pygame.K_r]:
            self.rotation_x = 0
            self.rotation_y = 0
            self.position_x = 0
            self.position_y = 0
            self.position_z = -8


def draw_coordinate_system():
    """Рисует оси координат"""
    glBegin(GL_LINES)

    # Ось X - красная
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(5, 0, 0)

    # Ось Y - зеленая
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 5, 0)

    # Ось Z - синяя
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 5)

    glEnd()


def draw_grid(size=700, step=1):
    """Рисует сетку на плоскости XZ"""
    glBegin(GL_LINES)
    glColor3f(0.3, 0.3, 0.3)  # Серый цвет

    for i in range(-size, size + 1, step):
        # Линии вдоль Z
        glVertex3f(i, 0, -size)
        glVertex3f(i, 0, size)
        # Линии вдоль X
        glVertex3f(-size, 0, i)
        glVertex3f(size, 0, i)

    glEnd()





def display_camera_info(camera):
    """Выводит информацию о положении камеры в заголовок окна"""
    info = f"Camera: Pos({camera.position_x:.1f}, {camera.position_y:.1f}, {camera.position_z:.1f}) Rot({camera.rotation_x:.1f}, {camera.rotation_y:.1f})"
    pygame.display.set_caption(info)


def main():
    rf = ReadFile("files/DepthMap_Test.dat")
    points = rf.read_dat_file()
    if(points==False):
        return
    points.move_to_center()
    points.norm_points()
    points.zoom_points(4)
    data, width, height=rf.read_dat_file2()
    print("123")
    vert, colors=points.get_vert_colors()
    vertices = np.array(vert, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)
    vbo_p = vbo.VBO(vertices)
    vbo_c=vbo.VBO(colors)
    print(len(vertices))


    pygame.init()
    display = (1600, 1200)
    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF | pygame.locals.OPENGL)
    pygame.display.set_caption("Управление камерой")

    # Настройка OpenGL
    glEnable(GL_DEPTH_TEST)

    # Создаем камеру
    camera = Camera()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обрабатываем клавиши
        camera.handle_keys()

        # Обновляем информацию о камере
        display_camera_info(camera)

        # Очистка экрана
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Применяем трансформации камеры
        camera.apply_transform()

        # Рисуем сцену
        draw_grid()
        draw_coordinate_system()

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        vbo_p.bind()
        glVertexPointer(3, GL_FLOAT, 0, vbo_p)
        vbo_p.unbind()

        vbo_c.bind()
        glColorPointer(3, GL_FLOAT, 0, vbo_c)
        vbo_c.unbind()


        glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)


        # Обновляем дисплей
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()