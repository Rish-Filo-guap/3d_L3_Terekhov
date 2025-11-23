import math

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
    
# отрисовка сцены
def show_scene(vertices, normals):
    vbo_v = vbo.VBO(vertices)
    vbo_n = vbo.VBO(normals)

    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF | pygame.locals.OPENGL)
    pygame.display.set_caption("Управление камерой")

    glEnable(GL_DEPTH_TEST)

    camera = Camera()

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

        # освещение
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT3)
        glEnable(GL_LIGHT4)

        light_pos = [5, 5, 5, 0.0]
        light_pos2 = [-5, 0, 5, 0.0]
        light_pos3 = [-5, -5, -5, 0.0]
        light_pos4 = [5, 0, -5, 0.0]

        # точки в местах освещения
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

        # полигоны
        vbo_v.bind()
        glVertexPointer(3, GL_FLOAT, 0, vbo_v)
        vbo_v.unbind()

        # нормали
        vbo_n.bind()
        glNormalPointer(GL_FLOAT, 0, vbo_n)
        vbo_n.unbind()

        glDrawArrays(GL_TRIANGLES, 0, len(vertices))

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        # Обновляем дисплей
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

