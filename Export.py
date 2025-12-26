import math
from typing import List, Tuple
from PIL import Image, ImageDraw
import numpy as np


def save_to_ascii_stl(filename, vert, norm):
    object_name = "object"
    with open(filename, 'w') as f:
        f.write(f"solid {object_name}\n\n")
        i=0
        while i< (len(vert)-6):
            for k in range(2):
                f.write(f"  facet normal {norm[3*k+i][0]} {norm[3*k+i][1]} {norm[3*k+i][2]}\n")
                # f.write(f"  facet normal {0} {0} {0}\n")
                f.write("    outer loop\n")
                for j in range(3):
                    f.write(f"      vertex {vert[3*k+(j)+i][0]} {vert[3*k+(j)+i][1]} {vert[3*k+(j)+i][2]}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n\n")
            i+=6


        f.write(f"endsolid {object_name}")


def save_to_obj(filename, vertices, normals):

    if len(vertices) % 3 != 0:
        raise ValueError("Количество координат вершин должно быть кратно 3")

    if len(normals) % 3 != 0:
        raise ValueError("Количество координат нормалей должно быть кратно 3")

    num_vertices = len(vertices)
    with open(filename, 'w') as f:


        # Запись вершин
        for v in vertices:
            x, y, z = v[0], v[1], v[2]
            f.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")

        f.write("\n")

        # Запись нормалей
        for n in normals:
            x, y, z = n[0], n[1], n[2]
            f.write(f"vn {x:.6f} {y:.6f} {z:.6f}\n")

        f.write("\n")

        # Запись полигонов
        for i in range(0, num_vertices, 3):
            v1_idx = i + 1
            v2_idx = i + 2
            v3_idx = i + 3

            # Записываем треугольник с нормалями
            f.write(f"f {v1_idx}//{v1_idx} {v2_idx}//{v2_idx} {v3_idx}//{v3_idx}\n")

        f.write("\n# End of file")
        print(f"Файл '{filename}' успешно создан.")


def save_to_ply(filename, vertices, colors, normals):

    num_vertices = len(vertices)
    num_faces = num_vertices // 3

    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write(f"element vertex {num_vertices}\n")
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property float nx\n")
        f.write("property float ny\n")
        f.write("property float nz\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("property uchar alpha\n")
        f.write(f"element face {num_faces}\n")
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")

        # Запись вершин с нормалями и цветами
        for i in range(num_vertices):
            v = vertices[i]
            n = normals[i]
            c = colors[i]

            # Проверка и нормализация цвета (0-255)
            if len(c) == 3:  # RGB
                r, g, b = c
                a = 255  # альфа по умолчанию
            else:
                raise ValueError(f"Цвет вершины {i} должен быть RGB")

            # Преобразование цвета в диапазон 0-255
            if isinstance(r, float) and r <= 1.0:
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
                a = int(a * 255) if isinstance(a, float) else a

            # Запись вершины
            f.write(f"{v[0]} {v[1]} {v[2]} {n[0]} {n[1]} {n[2]} {r} {g} {b} {a}\n")

        # Запись полигонов (треугольников)
        for i in range(num_faces):
            v0 = i * 3
            v1 = v0 + 1
            v2 = v0 + 2
            f.write(f"3 {v0} {v1} {v2}\n")


def export_p_bmp(file_path, vertices, colors, camera_pos):
    # Создаем изображение
    image = Image.new('RGB', (1000, 1000), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Конвертируем в numpy
    vertices = np.array(vertices, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)

    # 1. Создаем матрицу вида камеры
    camera_target = np.array([0, 0, 0])
    camera_up = np.array([0, 1, 0])
    camera_pos = np.array(camera_pos)

    # Векторы базиса камеры
    forward = camera_target - camera_pos
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, camera_up)
    right = right / np.linalg.norm(right)
    up = np.cross(right, forward)

    # Матрица вида
    view_matrix = np.array([
        [right[0], right[1], right[2], -np.dot(right, camera_pos)],
        [up[0], up[1], up[2], -np.dot(up, camera_pos)],
        [-forward[0], -forward[1], -forward[2], np.dot(forward, camera_pos)],
        [0, 0, 0, 1]
    ])

    # 2. Создаем матрицу перспективной проекции
    fov = 45
    aspect_ratio = 1.0
    near = 0.1
    far = 100.0

    fov_rad = np.radians(fov)
    tan_half_fov = np.tan(fov_rad / 2.0)

    projection_matrix = np.array([
        [1.0 / (aspect_ratio * tan_half_fov), 0, 0, 0],
        [0, 1.0 / tan_half_fov, 0, 0],
        [0, 0, -(far + near) / (far - near), -(2 * far * near) / (far - near)],
        [0, 0, -1, 0]
    ])

    # 3. Объединенное преобразование
    transform_matrix = np.dot(projection_matrix, view_matrix)

    # 4. Преобразуем вершины
    homogeneous_vertices = np.hstack([vertices, np.ones((len(vertices), 1))])
    transformed = np.dot(homogeneous_vertices, transform_matrix.T)

    # Перспективное деление
    w = transformed[:, 3]
    w[w == 0] = 1e-10
    ndc_coords = transformed[:, :3] / w[:, np.newaxis]

    # 5. Преобразуем в экранные координаты
    width, height = 1000, 1000
    screen_coords = np.zeros((len(ndc_coords), 2))
    screen_coords[:, 0] = (ndc_coords[:, 0] + 1) * 0.5 * width
    screen_coords[:, 1] = (1 - ndc_coords[:, 1]) * 0.5 * height


    # 6. Рендерим треугольники
    for i in range(0, len(vertices), 3):
        # Проверяем, находится ли треугольник в поле зрения
        if (ndc_coords[i, 2] > 1 or ndc_coords[i, 2] < -1 or
                ndc_coords[i + 1, 2] > 1 or ndc_coords[i + 1, 2] < -1 or
                ndc_coords[i + 2, 2] > 1 or ndc_coords[i + 2, 2] < -1):
            continue

        # Координаты для отрисовки
        x1, y1 = int(screen_coords[i, 0]), int(screen_coords[i, 1])
        x2, y2 = int(screen_coords[i + 1, 0]), int(screen_coords[i + 1, 1])
        x3, y3 = int(screen_coords[i + 2, 0]), int(screen_coords[i + 2, 1])

        # Пропускаем вырожденные треугольники
        if (x1 == x2 and y1 == y2) or (x2 == x3 and y2 == y3) or (x1 == x3 and y1 == y3):
            continue

        # Средний цвет
        # breakpoint()
        avg_r = 255 * ((colors[i, 0] + colors[i + 1, 0] + colors[i + 2, 0]) / 3)
        avg_g = 255 * ((colors[i, 1] + colors[i + 1, 1] + colors[i + 2, 1]) / 3)
        avg_b = 255 * ((colors[i, 2] + colors[i + 1, 2] + colors[i + 2, 2]) / 3)
        # Рисуем треугольник
        draw.polygon([(x1, y1), (x2, y2), (x3, y3)],
                     fill=(int(avg_r), int(avg_g), int(avg_b)))

    image.save(file_path, 'BMP')