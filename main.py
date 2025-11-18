import numpy as np
import pygame.locals

from Export import write_ascii_stl_with_normals
from View import *
from read_file import ReadFile


def main():
    rf = ReadFile("files/DepthMap_6.dat")
    points = rf.read_dat_file()
    if(points==False):
        return
    points.move_to_center()
    points.norm_points()
    points.zoom_points(4)

    vert, norm=points.calculate_arrays()
    vertices = np.array(vert, dtype=np.float32)
    normals = np.array(norm, dtype=np.float32)

    write_ascii_stl_with_normals("stl/file6.stl", vertices, normals)
    show_scene(vertices, normals)

    print(len(vertices))



if __name__ == "__main__":
    main()