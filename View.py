import math

import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo


class Camera:
    def __init__(self):

        self.rotation_x = 0  # Вращение вокруг оси X
        self.rotation_y = 0  # Вращение вокруг оси Y
        self.position_x = 0  # Позиция камеры по X
        self.position_y = 0  # Позиция камеры по Y
        self.position_z = -5  # Позиция камеры по Z
        self.rotation_speed = 3  # Скорость вращения
        self.move_speed = 0.1  # Скорость перемещения
        self.angle=0;

    def apply_transform(self):
        """Применяет трансформации камеры"""
        glLoadIdentity()
        gluPerspective(45, (800 / 600), 0.1, 5000.0)

        # Сначала перемещаем камеру, потом вращаем
        glTranslatef(self.position_x, self.position_y, self.position_z)

        glTranslatef(-self.position_x, -self.position_y, -self.position_z)
        glRotatef(self.rotation_x, 1, 0, 0)  # Вращение вокруг X
        glRotatef(self.rotation_y, 0, 1, 0)  # Вращение вокруг Y
        glTranslatef(self.position_x, self.position_y, self.position_z)

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

            self.position_x += math.sin(-self.rotation_y*math.pi/180)*self.move_speed
            self.position_z += math.cos(-self.rotation_y*(math.pi/180))*self.move_speed
            self.position_y += self.rotation_x*math.pi/180*self.move_speed
        if keys[pygame.K_s]:
            # Двигаемся назад (по оси Z)
            self.position_x -= math.sin(-self.rotation_y * math.pi / 180) * self.move_speed
            self.position_z -= math.cos(-self.rotation_y * (math.pi / 180)) * self.move_speed
            self.position_y -= self.rotation_x * math.pi / 180 * self.move_speed
        if keys[pygame.K_a]:
            # Двигаемся влево (по оси X)
            # self.position_x += self.move_speed
            self.position_x += math.sin(math.pi/2+self.rotation_y * math.pi / 180) * self.move_speed
            self.position_z -= math.cos(math.pi/2+self.rotation_y * (math.pi / 180)) * self.move_speed
        if keys[pygame.K_d]:
            # Двигаемся вправо (по оси X)
            self.position_x -= math.sin(math.pi / 2 + self.rotation_y * math.pi / 180) * self.move_speed
            self.position_z += math.cos(math.pi / 2 + self.rotation_y * (math.pi / 180)) * self.move_speed

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


def display_camera_info(camera):
    """Выводит информацию о положении камеры в заголовок окна"""
    info = f"Camera: Pos({camera.position_x:.1f}, {camera.position_y:.1f}, {camera.position_z:.1f}) Rot({camera.rotation_x:.1f}, {camera.rotation_y:.1f})"
    pygame.display.set_caption(info)
def show_scene(vertices, normals):
    vbo_v = vbo.VBO(vertices)
    vbo_n = vbo.VBO(normals)

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

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT3)
        glEnable(GL_LIGHT4)

        light_pos = [5, 5, 5, 0.0]
        light_pos2 = [-5, 0, 5, 0.0]
        light_pos3 = [-5, -5, -5, 0.0]
        light_pos4 = [5, 0, -5, 0.0]

        glPointSize(20)
        glBegin(GL_POINTS)
        glVertex3f(light_pos2[0], light_pos2[1], light_pos2[2])
        glVertex3f(light_pos[0], light_pos[1], light_pos[2])
        glVertex3f(light_pos3[0], light_pos3[1], light_pos3[2])
        glVertex3f(light_pos4[0], light_pos4[1], light_pos4[2])
        glEnd()

        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glLightfv(GL_LIGHT1, GL_POSITION, light_pos2)
        glLightfv(GL_LIGHT3, GL_POSITION, light_pos3)
        glLightfv(GL_LIGHT4, GL_POSITION, light_pos4)

        # Рисуем сцену

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        vbo_v.bind()
        glVertexPointer(3, GL_FLOAT, 0, vbo_v)
        vbo_v.unbind()

        vbo_n.bind()
        glNormalPointer(GL_FLOAT, 0, vbo_n)  # Указываем нормали
        vbo_n.unbind()

        glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        # Обновляем дисплей
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

