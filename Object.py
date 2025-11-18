import math


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
        self.normal = None
        self.vert = None
        self.width = width
        self.height = height
        self.points = points
        self.depth=0
        for i in range(self.height):
            for j in range(self.width):
                if (self.points[i][j].z > self.depth):
                    self.depth = self.points[i][j].z

    def _start_window(self):
        self.i = 0
        self.j = 0

    def _move_window(self):
        if (self.j > self.width - 2):
            self.j = 0
            self.i += 1
        if (self.i > self.height - 2):
            return False
        else:
            res=None
            # print(self.width,len(self.points[0]), self.j, self.height,len(self.points), self.i)
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

    def _calculate_normal(self, vertex1, vertex2, vertex3):

        u = [vertex2[0] - vertex3[0], vertex2[1] - vertex3[1], vertex2[2] - vertex3[2]]
        v = [vertex3[0] - vertex1[0], vertex3[1] - vertex1[1], vertex3[2] - vertex1[2]]

        normal = [
            u[1] * v[2] - u[2] * v[1],  # x
            u[2] * v[0] - u[0] * v[2],  # y
            u[0] * v[1] - u[1] * v[0]  # z
        ]

        # Нормализуем вектор
        length = math.sqrt(normal[0] ** 2 + normal[1] ** 2 + normal[2] ** 2)
        if length > 0:
            normal = [normal[0] / length, -normal[1] / length, -normal[2] / length]
        return normal

    def calculate_arrays(self):
        self.vert = []
        self.normal = []

        self._start_window()
        two_polygons = self.get_points_from_window()
        while two_polygons != False:
            firnormal=self._calculate_normal(two_polygons[0].get_point(), two_polygons[1].get_point(),two_polygons[2].get_point())
            secnormal=self._calculate_normal(two_polygons[3].get_point(), two_polygons[4].get_point(), two_polygons[5].get_point())

            for i, point in enumerate(two_polygons):
                self.vert.append(point.get_point())
                if (i / 3 >= 1):
                    self.normal.append(firnormal)
                else:
                    self.normal.append(secnormal)
            two_polygons = self.get_points_from_window()

        return self.vert, self.normal

