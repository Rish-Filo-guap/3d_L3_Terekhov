import math
import struct

from Object import Point, Points


class ReadFile:

    def __init__(self, filename):
        self.filename = filename

    def read_dat_file(self):
        try:
            with open(self.filename, 'rb') as file:
                # Читаем Height и Width
                height = int(struct.unpack('d', file.read(8))[0])
                width = int(struct.unpack('d', file.read(8))[0])

                # Читаем массив данных

                point_arr=[]
                for i in range(height):
                    row = []
                    for j in range(width):
                        # Читаем 8 байт (64 бита) для double
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
            print(f"Ошибка: Файл '{self.filename}' не найден")
            return False
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False