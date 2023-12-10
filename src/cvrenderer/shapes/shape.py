import math

import numpy

from src.cvrenderer.utils import *


class Shape:
    def __init__(self, x=0, y=0, z=0, x_rot=0, y_rot=0, z_rot=0):
        self.shape_points_homogeneous = None
        self.R_static = None
        self.verbose = None
        self.M = None
        self.T = None
        self.R = None
        self.x = x
        self.y = y
        self.z = z
        self.parent = None

        self.x_rot = x_rot
        self.y_rot = y_rot
        self.z_rot = z_rot

        self.rotate(self.x_rot, self.y_rot, self.z_rot)
        self.translate(self.x, self.y, self.z)

        self.calculate_transformation_matrix()

    def set_verbose(self, verbose=True):
        self.verbose = verbose

    def rotate(self, x_rot, y_rot, z_rot, order="xyz"):
        self.x_rot = x_rot
        self.y_rot = y_rot
        self.z_rot = z_rot
        self.R = get_rotation_matrix(x_rot, y_rot, z_rot, order=order)

    def translate(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.T = np.array([
            [self.x],
            [self.y],
            [self.z]
        ])

    def set_R_static(self, x_rot, y_rot, z_rot, order="xyz"):
        self.R_static = get_rotation_matrix(x_rot, y_rot, z_rot, order=order)

    def calculate_transformation_matrix(self):
        # Compute local M
        self.M = np.append(self.R, self.T, axis=1)
        self.M = np.append(self.M, np.array([[0.0, 0.0, 0.0, 1]]), axis=0)

        if (self.parent is not None) and (self.parent.R_static is not None):
            # 1. Get rotation matrix of the parent
            self.parent.calculate_transformation_matrix()
            M_P = self.parent.get_transformation_matrix()

            # self.M = M_P  # TODO: Works but only following parent movement
            self.M = M_P @ self.M # TODO: Ideally should be like this

        if self.verbose:
            print(
                f"r: {self.get_pos_norm()}, x: {self.x}, y: {self.y}, z: {self.z}, x_rot: {self.x_rot}, y_rot: {self.y_rot}, z_rot: {self.z_rot}")

    def get_pos_norm(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def get_transformation_matrix(self):
        return self.M

    def set_transformation_matrix(self, M):
        self.R = M[0:3, 0:3]
        self.T = M[:-1, -1][:, np.newaxis]
        self.M = M

    def get_points(self):
        self.calculate_transformation_matrix()
        pts = self.M @ self.shape_points_homogeneous.T
        return pts

    # Hierarchical stuff
    def attach_parent(self, parent) -> None:
        """
        We are gonna set a parent to this shape
        :param parent:
        """
        self.parent = parent

    def move_center(self, dx, dy, dz):
        move = np.array([dx, dy, dz])
        if self.shape_points_homogeneous is not None:
            for j, row in enumerate(self.shape_points):
                for i, col in enumerate(row):
                    self.shape_points[j][i] -= move[i]

            self.x -= dx
            self.y -= dy
            self.z -= dz

            self.shape_points_homogeneous = np.append(self.shape_points, np.ones((len(self.shape_points), 1)),
                                                      axis=1)
