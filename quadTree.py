# I am using QuadTree to optimize the neighbor loop
# It's a complex algorithm (I don't fully unserstand)
# Wikipedia itself didn't help, I give credit to all youtube videos I used in the readme file
from cmu_graphics import *

class Point:
    def __init__(self, x, y, data = None):
        self.x = x
        self.y = y
        self.data = data
        

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        
    def contains(self, point):
        # Checks if the point is inside this rectangle
        return (self.x <= point.x < self.x + self.w and
                self.y <= point.y < self.y + self.h)
        
    def intersects(self, other):
        # Checks if this rectangle intersects with another rectangle
        return not (
            other.x > self.x + self.w or
            other.x + other.w < self.x or
            other.y > self.y + self.h or
            other.y + other.h < self.y
        )
        
class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Rectangle
        self.capacity = capacity  # Max points per node
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w / 2, self.boundary.h / 2

        self.northwest = Quadtree(Rectangle(x, y, w, h), self.capacity)
        self.northeast = Quadtree(Rectangle(x + w, y, w, h), self.capacity)
        self.southwest = Quadtree(Rectangle(x, y + h, w, h), self.capacity)
        self.southeast = Quadtree(Rectangle(x + w, y + h, w, h), self.capacity)
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            return (self.northwest.insert(point) or
                    self.northeast.insert(point) or
                    self.southwest.insert(point) or
                    self.southeast.insert(point))

    def queryRange(self, range, found=None):
        if found is None:
            found = []

        if not self.boundary.intersects(range):
            return found

        for p in self.points:
            if range.contains(p):
                found.append(p)

        if self.divided:
            self.northwest.queryRange(range, found)
            self.northeast.queryRange(range, found)
            self.southwest.queryRange(range, found)
            self.southeast.queryRange(range, found)

        return found

    def clear(self):
        self.points = []
        self.divided = False
        if hasattr(self, 'northwest'):
            del self.northwest
            del self.northeast
            del self.southwest
            del self.southeast
            


# draw the quadtree
def drawQuadtreeGrid(quadtree):
    # Get this node's rectangle
    rect = quadtree.boundary

    # Draw this node's boundary
    drawRect(rounded(rect.x), rounded(rect.y), rounded(rect.w), rounded(rect.h), 
             fill = None, borderWidth = 1, border='gray')

    # If subdivided, recursively draw children
    if quadtree.divided:
        drawQuadtreeGrid(quadtree.northwest)
        drawQuadtreeGrid(quadtree.northeast)
        drawQuadtreeGrid(quadtree.southwest)
        drawQuadtreeGrid(quadtree.southeast)