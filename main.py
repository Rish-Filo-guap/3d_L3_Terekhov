import pygame
import pygame.locals
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from read_file import *

# Вершины куба (8 вершин, каждая по 3 координаты)
vertices = (
    (100, -100, -100),
    (100, 100, -100),
    (-100, 100, -100),
    (-100, -100, -100),
    (100, -100, 100),
    (100, 100, 100),
    (-100, -100, 100),
    (-100, 100, 100)
)

# Грани куба (6 граней, каждая из 4 вершин)
edges = (
    (0, 1, 2, 3),  # задняя грань
    (3, 2, 7, 6),  # левая грань
    (6, 7, 5, 4),  # передняя грань
    (4, 5, 1, 0),  # правая грань
    (1, 5, 7, 2),  # верхняя грань
    (4, 0, 3, 6)   # нижняя грань
)

# Цвета для каждой грани (RGB)
colors = (
    (1, 0, 0),  # красный
    (0, 1, 0),  # зеленый
    (0, 0, 1),  # синий
    (1, 1, 0),  # желтый
    (1, 0, 1),  # пурпурный
    (0, 1, 1)   # голубой
)

def draw_cube():
    """Рисует куб с цветными гранями"""
    glBegin(GL_QUADS)
    for i, face in enumerate(edges):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_point(x, y, z, size=5.0, color=(1.0, 1.0, 1.0)):
    """Рисует точку в указанных координатах"""
    glPointSize(size)  # Размер точки
    glColor3f(*color)  # Цвет точки

    glBegin(GL_POINTS)
    glVertex3f(x, y, z)
    glEnd()


def draw_points(points):
    """Рисует куб с цветными гранями"""
    glPointSize(10)
    glBegin(GL_POINTS)
    for i,point in enumerate(points):
        glVertex3fv(point)
        glColor3f(point[2],   1,1)
    glEnd()

def draw():
    draw_points(vertices)

def draw_object(data, height, width):
    glBegin(GL_TRIANGLES)
    glColor3f(1,0,1)
    i=0
    j=0
    while i<height-1:
        while j<width-1:
            if(data[i][j]!=0 and data[i+1][j]!=0 and data[i+1][j+1]!=0 and data[i][j+1]!=0):
                print(i,j)
                glColor3f(0, 1, 1)
                glVertex3f(i,j,data[i][j])
                glVertex3f(i+1,j,data[i+1][j])
                glVertex3f(i,j+1,data[i][j+1])

                glColor3f(1, 1, 0)
                glVertex3f(i + 1, j, data[i + 1][j])
                glVertex3f(i+1, j+1, data[i+1][j+1])
                glVertex3f(i, j + 1, data[i][j + 1])
            j+=2
        i+=2
        j=0

            # if ((data[i][j] > 0.0) & (data[i-1][j] > 0.0) & (data[i-1][j+1] > 0.0) & (data[i][j+1] > 0.0)):

    glEnd()



def main():
    rf= ReadFile("files/DepthMap_Test.dat")
    data, height, width=rf.read_dat_file()
    # data=[[-1.0, -2.0 -3.0],
    #       [1.0, 2.0, 3.0],
    #       [10.0, 20.0, 30.0]]
    # height=3
    # width=3
    points=rf.get_points()
    # print(points)
    # print(data)


    # Инициализация Pygame
    pygame.init()
    display = (1600, 1200)
    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF | pygame.locals.OPENGL)
    pygame.display.set_caption("Вращающийся куб - OpenGL")

    # Настройка перспективы
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Перемещаем камеру назад
    glTranslatef(300, 300, -500)

    # Включение теста глубины
    glEnable(GL_DEPTH_TEST)

    # Переменные для вращения
    clock = pygame.time.Clock()
    rotation_speed = 1  # градусов в кадр

    # Основной цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Очистка буфера цвета и глубины
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Вращение куба
        glRotatef(rotation_speed, 0, 1, 0)  # вращение вокруг оси (3,1,1)

        # Рисуем куб
        # draw()
        draw_points(points)
        draw_cube()
        # draw_object(data, height, width)
        # Обновление дисплея

        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":

    main()