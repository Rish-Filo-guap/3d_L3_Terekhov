from Export import write_ascii_stl
from View import *
from Read import *

def main():
    # чтение объекта
    points = read_dat_file("files/DepthMap_6.dat")
    if(points==False):
        return

    # подготовка объекта
    points.move_to_center()
    points.norm_points()
    vertices, normals=points.calculate_arrays()

    # экспорт
    write_ascii_stl("stl/file6.stl", vertices, normals)
    # визуализация
    show_scene(vertices, normals)

if __name__ == "__main__":
    main()