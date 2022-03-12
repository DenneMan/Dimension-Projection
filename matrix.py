from msilib.schema import _Validation_records
import sys, pygame, math
from globals import *

def close():
    pygame.quit()
    sys.exit()

def vecToMat(vec):
    if type(vec) != vec2 and type(vec) != vec3 and type(vec) != vec4 and type(vec) != vec5:
        print("Error: Cannot convert vec to mat")
        close()
    elif vec.dim == 2:
        return matrix([
            [vec.x],
            [vec.y]
        ])
    elif vec.dim == 3:
        return matrix([
            [vec.x],
            [vec.y],
            [vec.z]
        ])
    elif vec.dim == 4:
        return matrix([
            [vec.x],
            [vec.y],
            [vec.z],
            [vec.w]
        ])
    elif vec.dim == 5:
        return matrix([
            [vec.x],
            [vec.y],
            [vec.z],
            [vec.w],
            [vec.v]
        ])

def matToVec(mat):
    if mat.cols != 1 or type(mat) != matrix:
        print("Error: Cannot convert mat to vec")
        close()
    elif mat.rows == 2:
        return vec2(
            mat.matrix[0][0],
            mat.matrix[1][0]
        )
    elif mat.rows == 3:
        return vec3(
            mat.matrix[0][0],
            mat.matrix[1][0],
            mat.matrix[2][0]
        )
    elif mat.rows == 4:
        return vec4(
            mat.matrix[0][0],
            mat.matrix[1][0],
            mat.matrix[2][0],
            mat.matrix[3][0]
        )
    elif mat.rows == 5:
        return vec5(
            mat.matrix[0][0],
            mat.matrix[1][0],
            mat.matrix[2][0],
            mat.matrix[3][0],
            mat.matrix[4][0]
        )

def rotate(axis_1, axis_2, vec, degrees):
    radians = (degrees / 180) * math.pi
    sin = math.sin(radians)
    cos = math.cos(radians)
    rotation = []
    for row_i in range(vec.dim):
        row = []
        for col_i in range(vec.dim):
            if row_i == col_i == axis_1:
                row.append(cos)
            elif row_i == axis_1 and col_i == axis_2:
                row.append(-sin)
            elif row_i == axis_2 and col_i == axis_1:
                row.append(sin)
            elif row_i == col_i == axis_2:
                row.append(cos)
            elif row_i == col_i:
                row.append(1)
            else:
                row.append(0)
        rotation.append(row)
    return matToVec(matrix(rotation) * vec)

def viewTransform(vec):
    tmp_mat = matrix([
        [SCREENSIZE[0], 0],
        [0, SCREENSIZE[1]]
    ])
    tmp_vec = matToVec(tmp_mat * vec)
    tmp_vec = vec2(tmp_vec.x + OFFSET, tmp_vec.y + OFFSET)
    return tmp_vec

def make_perspective():
    a = SCREENSIZE[1] / SCREENSIZE[0]
    fov = 30
    znear = 0.01
    zfar = 1000
    f = 1/(math.tan(fov/2))
    z1 = zfar/(zfar-znear)
    z2 = -(zfar*znear)/(zfar-znear)
    return matrix([
        [a*f, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, z1, z2],
        [0, 0, 1, 0]
    ])

def perspective3D(vec):
    tmp_vec = vec4(vec.x, vec.y, vec.z + 2, 1)
    tmp_vec = matToVec(make_perspective() * tmp_vec)
    if tmp_vec.w > 0:
        tmp_vec = vec2(tmp_vec.x / tmp_vec.w, tmp_vec.y / tmp_vec.w) #, tmp_vec.z / tmp_vec.w
        return tmp_vec
    return None

def perspective4D(distance, vec):
    tmp_mat = matrix([
        [1 / (distance - vec.w), 0, 0, 0],
        [0, 1 / (distance - vec.w), 0, 0],
        [0, 0, 1 / (distance - vec.w), 0]
    ])
    return matToVec(tmp_mat * vec)

def perspective5D(distance, vec):
    tmp_mat = matrix([
        [1 / (distance - vec.v), 0, 0, 0, 0],
        [0, 1 / (distance - vec.v), 0, 0, 0],
        [0, 0, 1 / (distance - vec.v), 0, 0],
        [0, 0, 0, 1 / (distance - vec.v), 0]
    ])
    return matToVec(tmp_mat * vec)

def dist(p1, p2):
    if type(p1) == type(p2) == vec3: 
        a = (p1.x - p2.x) ** 2
        b = (p1.y - p2.y) ** 2
        c = (p1.z - p2.z) ** 2
        return math.sqrt(a + b + c)
    if type(p1) == type(p2) == vec4: 
        a = (p1.x - p2.x) ** 2
        b = (p1.y - p2.y) ** 2
        c = (p1.z - p2.z) ** 2
        d = (p1.w - p2.w) ** 2
        return math.sqrt(a + b + c + d)
    if type(p1) == type(p2) == vec5: 
        a = (p1.x - p2.x) ** 2
        b = (p1.y - p2.y) ** 2
        c = (p1.z - p2.z) ** 2
        d = (p1.w - p2.w) ** 2
        e = (p1.v - p2.v) ** 2
        return math.sqrt(a + b + c + d + e)

def connect(vec_1, vec_2, display):
    _p1 = None 
    _p2 = None
    if type(vec_1) == type(vec_2) == vec5:
        Vec4D_1 = perspective5D(2, vec_1)
        Vec3D_1 = perspective4D(2, Vec4D_1)
        Vec2D_1 = perspective3D(Vec3D_1)

        Vec4D_2 = perspective5D(2, vec_2)
        Vec3D_2 = perspective4D(2, Vec4D_2)
        Vec2D_2 = perspective3D(Vec3D_2)
    
    if type(vec_1) == type(vec_2) == vec4:
        Vec3D_1 = perspective4D(2, vec_1)
        Vec2D_1 = perspective3D(Vec3D_1)

        Vec3D_2 = perspective4D(2, vec_2)
        Vec2D_2 = perspective3D(Vec3D_2)

    if type(vec_1) == type(vec_2) == vec3: 
        Vec2D_1 = perspective3D(vec_1)

        Vec2D_2 = perspective3D(vec_2)

    if type(vec_1) == type(vec_2) == vec2: 
        _p1 = viewTransform(vec_1)
        _p2 = viewTransform(vec_2)
    
    if Vec2D_1 != None and Vec2D_2 != None:
        _p1 = viewTransform(Vec2D_1)
        _p2 = viewTransform(Vec2D_2)
    
    if _p1 != None and _p2 != None:
        pygame.draw.line(display, (255, 255, 255), (_p1.x, _p1.y), (_p2.x, _p2.y), 2)

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.dim = 2

    def draw(self, display):
        Vec2D = viewTransform(self)
        pygame.draw.circle(
            display, 
            (255, 255, 255), 
            (Vec2D.x, 
            Vec2D.y), 
            4
        )

    def __repr__(self):
        return f"{self.x}, \n{self.y}"

class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.dim = 3

    def draw(self, display):
        Vec2D = perspective3D(self)
        if Vec2D != None:
            Vec2D.draw(display)

    def __repr__(self):
        return f"{self.x}, \n{self.y}, \n{self.z}"

class vec4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

        self.dim = 4

        self.radius = 4

    def draw(self, display):
        Vec3D = perspective4D(2, self)
        Vec3D.draw(display)

    def __repr__(self):
        return f"{self.x}, \n{self.y}, \n{self.z}, \n{self.w}"

    def __mul__(self, other):
        return vec4(self.x * other, self.y * other, self.z * other, self.w * other)

class vec5:
    def __init__(self, x, y, z, w, v):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.v = v

        self.dim = 5

    def draw(self, display):
        Vec4D = perspective5D(2, self)
        Vec4D.draw(display)

    def __repr__(self):
        return f"{self.x}, \n{self.y}, \n{self.z}, \n{self.w}, \n{self.v}"

    def __mul__(self, other):
        return vec5(self.x * other, self.y * other, self.z * other, self.w * other, self.v * other)

class matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)

        tmp = []
        for row in matrix:
            tmp.append(len(row))
        if sum(tmp) / self.cols != self.rows:
            print("Error: can not have matrix with different columns per rows")
            close()
    
    def __mul__(self, other):
        if type(other) == vec2 or type(other) == vec3 or type(other) == vec4 or type(other) == vec5:
            other = vecToMat(other)
        
        if type(other) == int or type(other) == float:
            tmp_mat = []
            for row in self.matrix:
                tmp_row = []
                for i in row:
                    tmp_row.append(i * other)
                tmp_mat.append(tmp_row)
        elif type(other) == matrix:
            if self.cols != other.rows:
                print("Error: Columns of self must match rows of other")
                close()
            tmp_mat = []
            for i in range(self.rows):
                tmp_row = []
                for j in range(other.cols):
                    sum = 0
                    for k in range(self.rows):
                        sum += self.matrix[i][k] * other.matrix[k][j]
                    tmp_row.append(sum)
                tmp_mat.append(tmp_row)
        else:
            print("Error: Multiplication by type is not supported with matrix")
            close()
        
        return matrix(tmp_mat)

    def __repr__(self):
        tmp_str = ""
        for i in range(self.rows):
            tmp_str += str(self.matrix[i]) + "\n"
        return tmp_str

if __name__ == '__main__':
    import main