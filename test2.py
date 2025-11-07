import time

import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *

from read_file import ReadFile


class Camera:
    def __init__(self):
        self.rotation_x = 0  # Вращение вокруг оси X
        self.rotation_y = 0  # Вращение вокруг оси Y
        self.position_x = 0  # Позиция камеры по X
        self.position_y = 0  # Позиция камеры по Y
        self.position_z = -8  # Позиция камеры по Z
        self.rotation_speed = 10  # Скорость вращения
        self.move_speed = 30  # Скорость перемещения

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


# Вершины куба
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)

# Грани куба
edges = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

# Цвета граней
colors = (
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, 0, 1), (0, 1, 1)
)


def draw_cube():
    """Рисует куб с цветными гранями"""
    glBegin(GL_QUADS)
    for i, face in enumerate(edges):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_multiple_cubes():
    """Рисует несколько кубов в разных позициях"""
    # Центральный куб
    glPushMatrix()
    glTranslatef(0, 0, 0)
    draw_cube()
    glPopMatrix()

    # Кубы вокруг
    positions = [
        (3, 0, 0), (-3, 0, 0), (0, 3, 0), (0, -3, 0), (0, 0, 3), (0, 0, -3),
        (2, 2, 2), (-2, -2, -2), (2, -2, 2), (-2, 2, -2)
    ]

    for pos in positions:
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        glScalef(0.5, 0.5, 0.5)  # Уменьшаем размер
        draw_cube()
        glPopMatrix()


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


def draw_floor():
    """Рисует пол"""
    glBegin(GL_QUADS)
    glColor3f(0.2, 0.2, 0.2)  # Темно-серый цвет
    size = 20
    glVertex3f(-size, -2, -size)
    glVertex3f(-size, -2, size)
    glVertex3f(size, -2, size)
    glVertex3f(size, -2, -size)
    glEnd()

def draw_points():
    rf = ReadFile("files/DepthMap_6.dat")
    points = rf.get_points()
    glPointSize(10)
    glBegin(GL_POINTS)
    for i,point in enumerate(points):
        glVertex3fv(point)
        glColor3f(0,   1,1)
        # print(point)
    glEnd()

def draw_object(data, width, height):
    glBegin(GL_TRIANGLES)
    i=0
    j=0
    while i<height-1:
        while j<width-1:
            if(data[i][j]!=0 and data[i+1][j]!=0 and data[i+1][j+1]!=0 and data[i][j+1]!=0):
                # print(i,j)
                glColor3f(0, 1, 1)
                glVertex3f(i,j,data[i][j])
                glVertex3f((i+1),j,data[i+1][j])
                glVertex3f(i,(j+1),data[i][j+1])

                glColor3f(1, 1, 0)
                glVertex3f((i + 1), j, data[i + 1][j])
                glVertex3f((i+1), (j+1), data[i+1][j+1])
                glVertex3f(i, (j + 1), data[i][j + 1])
            j+=1
        i+=1
        j=0

            # if ((data[i][j] > 0.0) & (data[i-1][j] > 0.0) & (data[i-1][j+1] > 0.0) & (data[i][j+1] > 0.0)):

    glEnd()


def display_camera_info(camera):
    """Выводит информацию о положении камеры в заголовок окна"""
    info = f"Camera: Pos({camera.position_x:.1f}, {camera.position_y:.1f}, {camera.position_z:.1f}) Rot({camera.rotation_x:.1f}, {camera.rotation_y:.1f})"
    pygame.display.set_caption(info)


def main():
    rf = ReadFile("files/DepthMap_4.dat")
    points = rf.read_dat_file()
    if(points==False):
        return
    points.move_to_center()
    points.norm_points()
    data, width, height=rf.read_dat_file2()
    print("123")
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
        # draw_floor()
        draw_grid()
        draw_coordinate_system()
        draw_multiple_cubes()
        # draw_points()
        start = time.perf_counter()
        draw_object(data, width, height)
        end = time.perf_counter()
        print(f"Время выполнения draw_object(points): {end - start:.6f} секунд")
        # Обновляем дисплей
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()