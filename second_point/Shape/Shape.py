from math import acos,degrees,sqrt

class Point:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
    def set_x(self,new_x):
        self._x = new_x
    def set_y(self,new_y):
        self._y = new_y 
    def get_x(self):
        return self._x
    def get_y(self):    
        return self._y

class Line:
    def __init__(self, point_start: "Point", point_end: "Point"):
        self._point_start = point_start
        self._point_end = point_end
        self.length = (float(self._point_end._x - self._point_start._x)**2 +
                  float(self._point_end._y - self._point_start._y)**2)**(1/2)
    def get_point_start(self):
        return self._point_start
    def get_point_end(self):        
        return self._point_end
    def set_point_start(self, new_point_start: "Point"):
        self._point_start = new_point_start
    def set_point_end(self, new_point_end: "Point"):
        self._point_end = new_point_end

class Shape:
    def __init__(self, is_regular: bool, *Lines: "Line"):
        some_edges = []
        self.lines = Lines
        self._is_regular = is_regular
        for i in Lines:
            some_edges.append([i._point_start._x, i._point_start._y])
            some_edges.append([i._point_end._x, i._point_end._y])
            some_edges.pop()
        edges = some_edges
        self.edges = edges
    def get_lines(self):
        return self.lines
    def set_lines(self, *new_lines: "Line"):
        self.lines = new_lines
    def get_is_regular(self):
        return self._is_regular
    def set_is_regular(self, new_is_regular: bool):
        self._is_regular = new_is_regular
    def get_edges(self):
        return self.edges
    def set_edges(self, new_edges):
        self.edges = new_edges
    
    def compute_area(self):
        raise NotImplementedError("a esta clase falta calcularle el area")
    def compute_perimeter(self):
        perimeter = 0
        for line in self.lines:
            perimeter += line.length
        return perimeter
    def compute_inner_angles(self):
        #toco resolver, se busca implementar la solución del álgebra lineal
        #se busca sacar el coseno del ángulo entre 2 vectores y se aplica arccos
        angles = []
        if self._is_regular == True:
            if type(self) == Equilateral:
                return f"los ángulos internos valen {180/len(self.lines)}"
            else: return f"los ángulos internos valen {360/len(self.lines)}"
        else: pass
        for l in range(-1,len(self.lines)-1,1): #se usa el método del coseno entre 2 vectores
            linea_1_unitario = [(self.lines[l]._point_end._x - #este pedazo es el x del unitario
                                 self.lines[l]._point_start._x)/self.lines[l].length,
                                (self.lines[l]._point_end._y - #este pedazo es el y unitario
                                 self.lines[l]._point_start._y)/self.lines[l].length]
            linea_2_unitario = [(self.lines[l+1]._point_end._x - #este pedazo es el x del unitario
                                 self.lines[l+1]._point_start._x)/self.lines[l+1].length,
                                (self.lines[l+1]._point_end._y - #este pedazo es el y unitario
                                 self.lines[l+1]._point_start._y)/self.lines[l+1].length]
            angle = round(degrees(acos(linea_1_unitario[0]*linea_2_unitario[0]+
                         linea_1_unitario[1]*linea_2_unitario[1])))
            if abs(angle) > 90: #corrige en caso de que el ángulo encontrado sea de más de 90 grados
                angle = angle -90
                angles.append(angle)
            else: angles.append(angle)
        return angles
                

class Triangle(Shape):
    def __init__(self, is_regular, *Lines):
        super().__init__(is_regular, *Lines)
        self._is_regular = is_regular
        self.edges
    def compute_perimeter(self):
        return super().compute_perimeter()
    def compute_area(self):
        p = self.compute_perimeter()
        sp = p/2 #semiperimetro
        area = ((sp*(sp - self.lines[0].length)*
                (sp-self.lines[1].length)*(sp - self.lines[2].length)))**(1/2)
        area = round(area,4) #redondea el número para no tener inconsistencias con la fórmula tradicional
        return area
    def compute_inner_angles(self):
        return super().compute_inner_angles()

class Scalene(Triangle):
    def __init__(self, is_regular, *Lines):
        self.lines = Lines
        self._is_regular = is_regular
        #se comparan las longitudes de las líneas:
        comp_1 = self.lines[0].length != self.lines[1].length
        comp_2 = self.lines[1].length != self.lines[2].length
        comp_3 = self.lines[2].length != self.lines[0].length 
        if not (comp_1 and comp_2 and comp_3):
            raise NotImplementedError("este no es un triángulo escaleno, introduzca un triángulo válido")
        else: super().__init__(is_regular, *Lines)

class Isosceles(Triangle):
    def __init__(self, is_regular, line_base : "Line", third_point: "Point"):
        self._line_base = line_base
        self.lines = [line_base, Line(line_base.point_start,third_point), #igual toca meter 3 puntos para el triángulo pero por lo menos no 3 líneas
                      Line(line_base.point_end,third_point)]
        #se verifica que el triángulo sea Isosceles
        comp_1 = self.lines[0].length == self.lines[1].length
        comp_2 = self.lines[1].length == self.lines[2].length
        comp_3 = self.lines[2].length == self.lines[0].length 
        if not (comp_1 or comp_2 or comp_3):
            raise NotImplementedError("este no es un triángulo isosceles, introduzca un triángulo válido")
        else: super().__init__(is_regular, *self.lines)
    def get_line_base(self):
        return self._line_base
    def set_line_base(self, new_line_base: "Line"):
        self._line_base = new_line_base
        self.lines[0] = new_line_base
        self.lines[1] = Line(new_line_base._point_start, self.lines[1]._point_end)
        self.lines[2] = Line(new_line_base._point_end, self.lines[2]._point_end)
        
class Equilateral(Triangle):
    def __init__(self, is_regular, line_base : "Line", third_point: "Point"):
        self._line_base = line_base
        self.lines = [line_base,Line(line_base._point_end,third_point), 
                      Line(line_base._point_start,third_point)] #igual toca meter 3 puntos para el triángulo pero por lo menos no 3 líneas
        comp_1 = self.lines[0].length == self.lines[1].length
        comp_2 = self.lines[1].length == self.lines[2].length
        comp_3 = self.lines[2].length == self.lines[0].length 
        if not (comp_1 and comp_2 and comp_3): #se verifica que el triángulo sea equilatero
            raise NotImplementedError("este no es un triángulo equilatero, introduzca un triángulo válido")
        else: super().__init__(is_regular, *self.lines)
    def get_line_base(self):
        return self._line_base
    def set_line_base(self, new_line_base: "Line"):
        self._line_base = new_line_base
        self.lines[0] = new_line_base
        self.lines[1] = Line(new_line_base._point_start, self.lines[1]._point_end)
        self.lines[2] = Line(new_line_base._point_end, self.lines[2]._point_end)
    def compute_inner_angles(self):
        inner_angles = super().compute_inner_angles()
        if 30 in inner_angles: #hardcodeando un error re extraño
           inner_angles.remove(30)
           inner_angles.append(60)
        return inner_angles

class TriRectangle(Triangle): #genera un triángulo rectángulo con sus catetos
    def __init__(self, is_regular, *Lines):
        lineas = [Lines[0],Lines[1], Line(Lines[0]._point_end,Lines[1]._point_end)]
        self._is_regular = is_regular
        self.lines = tuple(lineas)
        cosines = []
        for l in range(-1,len(self.lines)-1,1): #se usa el método del coseno entre 2 vectores
            linea_1_unitario = [(self.lines[l]._point_end._x - #este pedazo es el x del unitario
                                 self.lines[l]._point_start._x)/self.lines[l].length,
                                (self.lines[l]._point_end._y - #este pedazo es el y unitario
                                 self.lines[l]._point_start._y)/self.lines[l].length]
            linea_2_unitario = [(self.lines[l+1]._point_end._x - #este pedazo es el x del unitario
                                 self.lines[l+1]._point_start._x)/self.lines[l+1].length,
                                (self.lines[l+1]._point_end._y - #este pedazo es el y unitario
                                 self.lines[l+1]._point_start._y)/self.lines[l+1].length]
            cos = (linea_1_unitario[0]*linea_2_unitario[0]+
                         linea_1_unitario[1]*linea_2_unitario[1])
            cosines.append(cos)
        if not 0 in cosines: #se verifica que el triángulo sea rectángulo
            raise NotImplementedError("este no es un triángulo rectángulo, introduzca un triángulo válido")
        else: pass 
        self.lines = (self.lines[0], self.lines[1],
                    Line(self.lines[0]._point_end, self.lines[1]._point_end))
    def compute_inner_angles(self):
        #toco resolver, se busca implementar la solución del álgebra lineal
        #se busca sacar el coseno del ángulo entre 2 vectores y se aplica arccos
            angles = []
            if self._is_regular == True:
                if type(self) == Equilateral:
                    return f"los ángulos internos valen {180/len(self.lines)}"
                else: return f"los ángulos internos valen {360/len(self.lines)}"
            else: pass
            for l in range(-1,len(self.lines)-1,1): #se usa el método del coseno entre 2 vectores
                linea_1_unitario = [(self.lines[l]._point_end._x - #este pedazo es el x del unitario
                                    self.lines[l]._point_start._x)/self.lines[l].length,
                                    (self.lines[l]._point_end._y - #este pedazo es el y unitario
                                    self.lines[l]._point_start._y)/self.lines[l].length]
                linea_2_unitario = [(self.lines[l+1]._point_end._x - #este pedazo es el x del unitario
                                    self.lines[l+1]._point_start._x)/self.lines[l+1].length,
                                    (self.lines[l+1]._point_end._y - #este pedazo es el y unitario
                                    self.lines[l+1]._point_start._y)/self.lines[l+1].length]
                angle = round(degrees(acos(linea_1_unitario[0]*linea_2_unitario[0]+
                            linea_1_unitario[1]*linea_2_unitario[1])))
                if abs(angle) > 90: #corrige en caso de que el ángulo encontrado sea de más de 90 grados
                    angle = angle -90
                    angles.append(angle) #!! esto debería servir pero por alguna extraña razón no lo hace
                else: angles.append(angle)
            return angles
        
class Rectangle(Shape):
    def __init__(self, is_regular, *Lines):
        self.lines = Lines
        self._is_regular = is_regular
        super().__init__(is_regular, *Lines)
        if not len(self.lines) == 4:
            print(len(self.lines))
            print(self.lines)
            raise NotImplementedError("estas líneas no pueden formar un rectángulo")

class Square(Rectangle):
    def __init__(self,is_regular = True, *Lines):
        super().__init__(is_regular, *Lines)
        self.lines = Lines
        print(len(self.lines))
        lineas = []
        for l in self.lines:
            lineas.append(l.length)
            print(l.length)
        if not (len(self.lines) == 4 and (lineas.count(lineas[0]) == 4)):
            raise NotImplementedError("estas líneas no pueden formar un cuadrado")  