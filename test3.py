import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

def init_pygame():
    """Инициализация Pygame и OpenGL"""
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("OpenGL Pyramid Rendering")

    # Настройка OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Настройка перспективы
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

class TriangleRenderer:
    def __init__(self, vertices):
        """
        Инициализация рендерера с массивом вершин

        Args:
            vertices: numpy массив вершин shape=(n, 3)
        """
        self.vertices = np.array(vertices, dtype=np.float32)

        # Создание Vertex Buffer Object (VBO)
        self.vbo = vbo.VBO(self.vertices)

        # Количество треугольников
        self.triangle_count = len(vertices) // 3

    def draw(self, color=(1.0, 1.0, 1.0)):
        """Отрисовка треугольников с использованием VBO"""
        glColor3f(*color)

        self.vbo.bind()
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vbo)

        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))

        glDisableClientState(GL_VERTEX_ARRAY)
        self.vbo.unbind()

def create_pyramid():
    """Создание вершин пирамиды"""
    return [
        # Основание
        [-1, -1, -1], [1, -1, -1], [0, -1, 1],
        [-1, -1, -1], [0, -1, 1], [-1, -1, 1],

        # Боковые грани
        [-1, -1, -1], [1, -1, -1], [0, 1, 0],  # передняя
        [1, -1, -1], [0, -1, 1], [0, 1, 0],    # правая
        [0, -1, 1], [-1, -1, -1], [0, 1, 0],   # левая
    ]

def main_advanced():
    init_pygame()

    # Создание рендерера для пирамиды
    pyramid_vertices = create_pyramid()
    renderer = TriangleRenderer(pyramid_vertices)

    clock = pygame.time.Clock()
    rotation = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(rotation, 0, 1, 0)

        # Отрисовка с использованием VBO
        renderer.draw((0.8, 0.3, 0.2))

        pygame.display.flip()
        rotation += 1
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_advanced()