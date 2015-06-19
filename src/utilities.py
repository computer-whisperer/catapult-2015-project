import math

# The following was shamelessly stolen from stackoverflow and then extended to
# include operator support:
# http://stackoverflow.com/questions/20924085/python-conversion-between-coordinates

def rect(r, theta):
    """theta in degrees

    returns tuple; (float, float); (x,y)
    """
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y

def polar(x, y):
    """returns r, theta(degrees)
    """
    r = (x ** 2 + y ** 2) ** .5
    theta = math.degrees(math.atan2(y, x))
    return r, theta

class Vector2D(object):

    def __init__(self, x=None, y=None, r=None, theta=None):
        """x and y or r and theta(degrees)
        """
        if x is not None and y is not None:
            self.c_polar(x, y)
        elif r is not None and theta is not None:
            self.c_rect(r, theta)
        else:
            self.c_polar(0, 0)

    def c_polar(self, x, y, f = polar):
        self._x = x
        self._y = y
        self._r, self._theta = f(self._x, self._y)
        self._theta_radians = math.radians(self._theta)

    def c_rect(self, r, theta, f = rect):
        """theta in degrees
        """
        self._r = r
        self._theta = theta
        self._theta_radians = math.radians(theta)
        self._x, self._y = f(self._r, self._theta)

    def setx(self, x):
        self.c_polar(x, self._y)

    def getx(self):
        return self._x

    x = property(fget = getx, fset = setx)

    def sety(self, y):
        self.c_polar(self._x, y)

    def gety(self):
        return self._y

    y = property(fget=gety, fset=sety)

    def setxy(self, x, y):
        self.c_polar(x, y)

    def getxy(self):
        return self._x, self._y

    xy = property(fget=getxy, fset=setxy)

    def setr(self, r):
        self.c_rect(r, self._theta)

    def getr(self):
        return self._r

    r = property(fget=getr, fset=setr)

    def settheta(self, theta):
        """theta in degrees
        """
        self.c_rect(self._r, theta)

    def gettheta(self):
        return self._theta

    theta = property(fget = gettheta, fset = settheta)

    def set_r_theta(self, r, theta):
        """theta in degrees
        """
        self.c_rect(r, theta)

    def get_r_theta(self):
        return self._r, self._theta

    def clone(self):
        return Vector2D(self.x, self.y)

    r_theta = property(fget = get_r_theta, fset = set_r_theta)

    def __str__(self):
        return '({},{})'.format(self._x, self._y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2D(self._x*other, self._y*other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return Vector2D.__mul__(self, other)

    def __add__(self, other):
        if hasattr(other, "x") and hasattr(other, "y"):
            return Vector2D(self._x+other.x, self._y+other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        if hasattr(other, "x") and hasattr(other, "y"):
            return Vector2D(self._x-other.x, self._y-other.y)
        else:
            return NotImplemented
