import math

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


def calculate_normal(vertex1, vertex2, vertex3):
    """
    Вычисление нормали треугольника по трем вершинам
    используя векторное произведение
    """
    # Векторы сторон треугольника
    u = [vertex2[0] - vertex1[0], vertex2[1] - vertex1[1], vertex2[2] - vertex1[2]]
    v = [vertex3[0] - vertex1[0], vertex3[1] - vertex1[1], vertex3[2] - vertex1[2]]

    # Векторное произведение u x v
    normal = [
        u[1] * v[2] - u[2] * v[1],  # x
        u[2] * v[0] - u[0] * v[2],  # y
        u[0] * v[1] - u[1] * v[0]  # z
    ]

    # Нормализуем вектор
    length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
    if length > 0:
        normal = [normal[0] / length, normal[1] / length, normal[2] / length]

    return normal


def write_ascii_stl_with_normals(filename, vert, object_name="object"):
    """
    Запись STL файла в ASCII формате с расчетом нормалей
    meshes - список мешей, каждый меш - список треугольников
    """
    with open(filename, 'w') as f:
        f.write(f"solid {object_name}\n\n")
        i=0
        while i< (len(vert)-6):
            normal=[]
            normal.append(calculate_normal(vert[i],vert[i+1],vert[i+2]))
            normal.append(calculate_normal(vert[i+3],vert[i+4],vert[i+5]))
            for k in range(2):
                f.write(f"  facet normal {normal[k][0]} {normal[k][1]} {normal[k][2]}\n")
                # f.write(f"  facet normal -1.0 0 0\n")
                f.write("    outer loop\n")

                for j in range(3):
                    f.write(f"      vertex {vert[3*k+j+i][0]} {vert[3*k+j+i][1]} {vert[3*k+j+i][2]}\n")
                    # print(3*k+j+i)

                f.write("    endloop\n")
                f.write("  endfacet\n\n")
            i+=6


        f.write(f"endsolid {object_name}")


def main():
    rf = ReadFile("files/DepthMap_5.dat")
    points = rf.read_dat_file()
    if(points==False):
        return
    # points.move_to_center()
    # points.norm_points()
    # points.zoom_points(4)
    data, width, height=rf.read_dat_file2()
    print("123")
    vert, colors=points.get_vert_colors()
    vertices = np.array(vert, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)
    vbo_p = vbo.VBO(vertices)
    vbo_c=vbo.VBO(colors)
    print(len(vertices))
    write_ascii_stl_with_normals("stl/file.stl", vert)

    pygame.init()
    display = (1200, 800)
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

        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)
        # glEnable(GL_LIGHT1)
        # glEnable(GL_LIGHT2)
        light_pos = [1, 1, 1, 0.0]

        lamp_position = [-100, -100, 0, 1.0]  # Позиция
        lamp_position2 = [0, 100, 100, 1.0]  # Позиция
        lamp_diffuse = [0.9, 0.9, 0.6, 1.0]  # Теплый свет
        lamp_diffuse2 = [0.6, 0.9, 0.9, 1.0]  # Теплый свет
        lamp_specular = [1.0, 1.0, 0.8, 1.0]
        lamp_specular2 = [1.0, 1.0, 0.8, 1.0]

        glLightfv(GL_LIGHT1, GL_POSITION, lamp_position)
        glLightfv(GL_LIGHT2, GL_POSITION, lamp_position2)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, lamp_diffuse)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, lamp_diffuse2)
        glLightfv(GL_LIGHT1, GL_SPECULAR, lamp_specular)
        glLightfv(GL_LIGHT2, GL_SPECULAR, lamp_specular2)


        # glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

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