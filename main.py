from Export import *
from LightMethods import *
from View import *
from Read import *
from ReadJSON import *
import numpy as np
def main():

    readJSON=ReadJSON("jsons/config.json")
    points = read_dat_file(readJSON.depth_path)

    points.move_to_center()
    points.norm_points()
    points.calculate_vertices_and_normals()

    light_pos=readJSON.light_position
    camera_pos=readJSON.camera_position
    vectors={'light':light_pos, 'camera':camera_pos}


    if readJSON.reflection_model=="Ламберт":
        points.calculate_light(lambert_lighting, vectors)
    elif readJSON.reflection_model=="Фонг-Блинн":
        points.calculate_light(phong_blinn_lighting, vectors)
    elif readJSON.reflection_model=="Торенс-Сперроу":
        points.calculate_light(torrance_sparrow_illumination, vectors)
    else:
        print("неверная модель освещения")
        return


    vertices=np.array([point.get_point() for point in points.vert], dtype=np.float32)
    normals=np.array([point.normal for point in points.vert], dtype=np.float32)
    colors=np.array([point.color for point in points.vert], dtype=np.float32)



    # экспорт
    file_type=readJSON.save_model_path.split('.')[1]

    if file_type=='stl':
        save_to_ascii_stl(readJSON.save_model_path, vertices, normals)
    elif file_type=='obj':
        save_to_obj(readJSON.save_model_path, vertices, normals)
    elif file_type=='ply':
        save_to_ply(readJSON.save_model_path, vertices, normals)
    else:
        print("неверный тип файла")
        return


    print(colors)
    export_p_bmp(readJSON.save_im_path,vertices, colors, camera_pos)
    # save_to_obj('export/models/tes1.obj', vertices, normals)
    # save_to_ply(vertices, colors, normals,'export/models/tes1.ply')
    # save_to_obj(vertices, colors, normals,'export/models/tes1.obj')


    show_scene(vertices, normals, colors, light_pos)

if __name__ == "__main__":
    main()