def write_ascii_stl_with_normals(filename, vert,norm, object_name="object"):
    with open(filename, 'w') as f:
        f.write(f"solid {object_name}\n\n")
        i=0
        while i< (len(vert)-6):
            for k in range(2):
                f.write(f"  facet normal {norm[3*k+i][0]} {norm[3*k+i][1]} {norm[3*k+i][2]}\n")
                f.write("    outer loop\n")
                for j in range(3):
                    f.write(f"      vertex {vert[3*k+j+i][0]} {vert[3*k+j+i][1]} {vert[3*k+j+i][2]}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n\n")
            i+=6


        f.write(f"endsolid {object_name}")