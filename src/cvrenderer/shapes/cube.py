from ..shapes.shape import Shape
import numpy as np


class Cube(Shape):
    def __init__(self, x=0, y=0, z=0, w=1, h=1, l=1, x_rot=0, y_rot=0, z_rot=0, color=(0, 0, 0), thickness=1):
        Shape.__init__(self, x, y, z, x_rot, y_rot, z_rot)

        # Width, height and depth
        self.w = w
        self.h = h
        self.l = l
        self.name = "CUBE"

        self.color = color
        self.color_static = color
        self.grey = (50, 50, 50)
        self.thickness = thickness

        # Vertices of the cube
        self.shape_points = np.array([
            [-self.w / 2, -self.h / 2, -self.l / 2],
            [self.w / 2, -self.h / 2, -self.l / 2],
            [self.w / 2, self.h / 2, -self.l / 2],
            [-self.w / 2, self.h / 2, -self.l / 2],

            [-self.w / 2, -self.h / 2, self.l / 2],
            [self.w / 2, -self.h / 2, self.l / 2],
            [self.w / 2, self.h / 2, self.l / 2],
            [-self.w / 2, self.h / 2, self.l / 2]
        ])

        # Append one at the end of each row, TODO: WHY?
        self.shape_points_homogeneous = np.append(self.shape_points, np.ones((len(self.shape_points), 1)), axis=1)

    def set_scale(self, w, h, l):

        # Scale width, height and depth
        self.w = w
        self.h = h
        self.l = l

        self.shape_points = np.array([
            [-self.w / 2, -self.h / 2, -self.l / 2],
            [self.w / 2, -self.h / 2, -self.l / 2],
            [self.w / 2, self.h / 2, -self.l / 2],
            [-self.w / 2, self.h / 2, -self.l / 2],

            [-self.w / 2, -self.h / 2, self.l / 2],
            [self.w / 2, -self.h / 2, self.l / 2],
            [self.w / 2, self.h / 2, self.l / 2],
            [-self.w / 2, self.h / 2, self.l / 2]
        ])

        self.shape_points_homogeneous = np.append(self.shape_points, np.ones((len(self.shape_points), 1)), axis=1)
