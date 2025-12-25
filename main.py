from Export import write_ascii_stl
from View import *
from Read import *
from ReadJSON import *

def main():

    readJSON=ReadJSON("jsons/config.json")
    points = read_dat_file(readJSON.depth_path)
    # чтение объекта
    # if(points==False):
    #     return
    #
    # подготовка объекта
    points.move_to_center()
    points.norm_points()
    vertices, normals=points.calculate_arrays()

    # экспорт
    write_ascii_stl(readJSON.save_model_path, vertices, normals)
    # визуализация
    show_scene(vertices, normals)

if __name__ == "__main__":
    main()