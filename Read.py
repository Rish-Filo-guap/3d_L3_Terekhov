import struct

from Object import Point, Points

def read_dat_file(filename):
    try:
        with open(filename, 'rb') as file:
            height = int(struct.unpack('d', file.read(8))[0])
            width = int(struct.unpack('d', file.read(8))[0])


            point_arr=[]
            for i in range(height):
                row = []
                for j in range(width):
                    bytes_data = file.read(8)
                    if len(bytes_data) < 8:
                        raise ValueError("Недостаточно данных в файле")
                    value = struct.unpack('d', bytes_data)[0]
                    # row.append(Point(width-1-j,height-1-i,value))
                    row.append(Point(j,height-1-i,value))

                point_arr.append(row)
            points=Points(width,height, point_arr)
            return points

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        return False
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return False