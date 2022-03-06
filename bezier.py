# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 10:47:25 2022

@author: Connor
"""

import numpy as np
import matplotlib.pyplot as plt

# TODO:
# Have them be dragable
# While dragging, redraw the bezier curve connecting p1, p2, c1, c2

_PICK_RADIUS = 1

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if np.isreal(x):
            self._x = x
        else:
            raise ValueError(
                f"x must be a real number! (x = {x})")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if np.isreal(y):
            self._y = y
        else:
            raise ValueError(
                f"y must be a real number! (y = {y})")

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def plot(self, *args, ax=None, **kwargs):
        if ax == None:
            return plt.plot([self.x], [self.y], *args, **kwargs)
        else:
            return ax.plot([self.x], [self.y], *args, **kwargs)

class LineSegment:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, p1: Point):
        if isinstance(p1, Point):
            self._p1 = p1
        else:
            raise ValueError(f"Must be of type Point! ({type(p1)} != {type(Point)})")

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, p2: Point):
        if isinstance(p2, Point):
            self._p2 = p2
        else:
            raise ValueError(f"Must be of type Point! ({type(p2)} != {type(Point)})")

    def __repr__(self):
        return f"(p1: {self.p1}, p2: {self.p2})"

    def plot(self, *args, ax=None, **kwargs):
        if ax == None:
            self.p1.plot("o", picker=True, pickradius=_PICK_RADIUS, **kwargs)
            self.p2.plot("o", picker=True, pickradius=_PICK_RADIUS, **kwargs)
            return plt.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], *args, **kwargs)
        else:
            self.p1.plot("o", ax=ax, picker=True, pickradius=_PICK_RADIUS, **kwargs)
            self.p2.plot("o", ax=ax, picker=True, pickradius=_PICK_RADIUS, **kwargs)
            return ax.plot([self.p1.x, self.p2.x], [self.p1.y, self.p2.y], *args, **kwargs)
        if ax == None:
            return
        else:
            return

class BezierLineSegment(LineSegment):
    def __init__(self, p1, p2, c1=None, c2=None):
        super().__init__(p1, p2)
        self.c1 = c1
        self.c2 = c2

    @property
    def c1(self):
        return self._c1

    @c1.setter
    def c1(self, c1: Point):
        if isinstance(c1, Point):
            self._c1 = c1
        elif isinstance(c1, type(None)):
            self._c1 = self.p1
        else:
            raise ValueError(f"Must be of type Point! ({type(c1)} != {type(Point)})")

    @property
    def c2(self):
        return self._c2

    @c2.setter
    def c2(self, c2: Point):
        if isinstance(c2, Point):
            self._c2 = c2
        elif isinstance(c2, type(None)):
            self._c2 = self.p2
        else:
            raise ValueError(f"Must be of type Point! ({type(c2)} != {type(Point)})")

    def __repr__(self):
        return f"(p1: {self.p1}, c1: {self.c1}, c2: {self.c2}, p2: {self.p2})"

    def plot(self, *args, ax=None, **kwargs):
        tt = np.arange(0, 1.005, 0.01)
        xx = (1 - tt)**3 * self.p1.x
        xx += 3 * tt * (1 - tt)**2 * self.c1.x
        xx += 3 * (1 - tt) * tt**2 * self.c2.x
        xx += tt**3 * self.p2.x

        yy = (1 - tt)**3 * self.p1.y
        yy += 3 * tt * (1 - tt)**2 * self.c1.y
        yy += 3 * (1 - tt) * tt**2 * self.c2.y
        yy += tt**3 * self.p2.y
        if ax == None:
            ls1 = LineSegment(self.p1, self.c1)
            ls1.plot(color="g", linewidth=1)
            self.c1.plot("go", picker=True, pickradius=_PICK_RADIUS)
            ls2 = LineSegment(self.c2, self.p2)
            ls2.plot(color="g", linewidth=1)
            self.c2.plot("go", picker=True, pickradius=_PICK_RADIUS)
            return plt.plot(xx, yy, *args, **kwargs)
        else:
            ls1 = LineSegment(self.p1, self.c1)
            ls1.plot(ax=ax, linewidth=1, **kwargs)
            self.p1.plot("o", ax=ax, picker=True, pickradius=_PICK_RADIUS, **kwargs)
            self.c1.plot("o", ax=ax, picker=True, pickradius=_PICK_RADIUS, **kwargs)
            ls2 = LineSegment(self.c2, self.p2)
            ls2.plot(ax=ax, linewidth=1, **kwargs)
            self.p2.plot("o", ax=ax, picker=True, pickradius=_PICK_RADIUS, **kwargs)
            self.c2.plot("o", ax=ax, picker=True, pickradius=_PICK_RADIUS, **kwargs)
            return ax.plot(xx, yy, *args, **kwargs)


def onpick(event):
    print(event)
    return event
    # n = len(event.ind)
    # if not n:
    #     return
    # fig, axs = plt.subplots(n, squeeze=False)
    # for dataind, ax in zip(event.ind, axs.flat):
    #     ax.plot(X[dataind])
    #     ax.text(0.05, 0.9,
    #             f"$\\mu$={xs[dataind]:1.3f}\n$\\sigma$={ys[dataind]:1.3f}",
    #             transform=ax.transAxes, verticalalignment='top')
    #     ax.set_ylim(-0.5, 1.5)
    # fig.show()
    # return True


if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    c1 = Point(0.25, 0)
    c2 = Point(0.75, 1)

    l1 = LineSegment(p1, p2)
    bl1 = BezierLineSegment(p1, p2, c1, c2)

    plt.close("all")
    fig, ax = plt.subplots()
    ax.set_title('Click on Control Points :)')
    bl1.plot(ax=ax, color="g")
    l1.plot(ax=ax, color="b")
    fig.canvas.mpl_connect('pick_event', onpick)
    plt.show()
