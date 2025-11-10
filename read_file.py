import struct


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def zoom(self, k):
        if(self.z!=0):
            self.x = self.x * k
            self.y = self.y * k
            self.z = self.z * k
    def move(self, point):
        if(self.z!=0):
            self.x = self.x + point.x
            self.y = self.y + point.y
            self.z = self.z + point.z
    def get_point(self):
        return [self.x, self.y, self.z]
class Points:
    def __init__(self, width, height, points):
        self.width = width
        self.height = height
        self.points = points
        self.depth=0
        for i in range(self.height):
            for j in range(self.width):
                if (self.points[i][j].z > self.depth):
                    self.depth = self.points[i][j].z

    def start_window(self):
        self.i = 0
        self.j = 0

    def _move_window(self):
        if (self.j > self.width - 1):
            self.j = 0
            self.i += 1
        if (self.i > self.height - 1):
            return False
        else:
            res=None
            if (self.points[self.i][self.j].z != 0 and self.points[self.i + 1][self.j + 1].z != 0 and self.points[self.i + 1][self.j].z != 0 and self.points[self.i][self.j + 1].z != 0):
                res=[self.points[self.i][self.j], self.points[self.i+1][self.j], self.points[self.i][self.j+1],
                        self.points[self.i+1][self.j], self.points[self.i+1][self.j+1], self.points[self.i][self.j+1]]
            self.j+=1
            return res
    def get_points_from_window(self):
        while (True):
            tmp=self._move_window()
            if(tmp!=None):
                return tmp
            if(tmp==False):
                return False

    def zoom_points(self, k):
        for i in range(self.height):
            for j in range(self.width):
                self.points[i][j].zoom(k)
    def move_points(self, point):
        for i in range(self.height):
            for j in range(self.width):
                self.points[i][j].move(point)
    def norm_points(self):
        max_v=max(self.depth, self.width, self.height)
        if(max_v>1):
            self.zoom_points(1/max_v)
        print("norm_zoom= "+ str(max_v)+" "+str(1/max_v))
    def move_to_center(self):
        self.move_points(Point(-self.width/2, -self.height/2, -self.depth/2))
    def get_vert_colors(self):
        vert=[]
        colors=[]

        depth = 1
        for i in range(self.height):
            for j in range(self.width):
                if (self.points[i][j].z > depth):
                    depth = self.points[i][j].z

        self.start_window()
        two_polygons=self.get_points_from_window()
        while two_polygons != False:
            for i,pol in enumerate(two_polygons):
                vert.append(pol.get_point())
                if(i/3>=1):
                    colors.append([pol.z*(1/depth)-0.3,1,pol.z*(1/depth)-0.3])
                else:
                    # colors.append([1,pol.z*(1/depth)-0.3,pol.z*(1/depth)-0.3])
                    colors.append([pol.z*(1/depth)-0.3,1,pol.z*(1/depth)-0.3])
            two_polygons = self.get_points_from_window()
        return vert, colors



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
                        value = -struct.unpack('d', bytes_data)[0]
                        row.append(Point(j,i,value))
                    point_arr.append(row)

                points=Points(width, height, point_arr)
                return points

        except FileNotFoundError:
            print(f"Ошибка: Файл '{self.filename}' не найден")
            return False
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False
    def read_dat_file2(self):
        try:
            with open(self.filename, 'rb') as file:
                # Читаем Height и Width
                height = int(struct.unpack('d', file.read(8))[0])
                width = int(struct.unpack('d', file.read(8))[0])

                # Читаем массив данных

                points_arr=[]
                for i in range(height):
                    row = []
                    for j in range(width):
                        # Читаем 8 байт (64 бита) для double
                        bytes_data = file.read(8)
                        if len(bytes_data) < 8:
                            raise ValueError("Недостаточно данных в файле")
                        value = -struct.unpack('d', bytes_data)[0]
                        row.append(value)
                    points_arr.append(row)


                return points_arr, width, height

        except FileNotFoundError:
            print(f"Ошибка: Файл '{self.filename}' не найден")
            return False
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False
