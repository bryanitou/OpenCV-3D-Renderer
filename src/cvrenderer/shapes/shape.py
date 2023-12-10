import math

import numpy as np

from src.cvrenderer.utils import *


class Shape:
    def __init__(self, x=0, y=0, z=0, x_rot=0, y_rot=0, z_rot=0):
        self.R_static = None
        self.verbose = None
        self.M = None
        self.T = None
        self.R = None
        self.abs_sys_ref = False
        self.x = x
        self.y = y
        self.z = z

        self.x_rot = x_rot
        self.y_rot = y_rot
        self.z_rot = z_rot

        self.rotate(self.x_rot, self.y_rot, self.z_rot)
        self.translate(self.x, self.y, self.z)

        self.calculate_transformation_matrix()

    def set_static_rotation_matrix(self, x_rot=0, y_rot=0, z_rot=0, order="xyz"):
        self.R_static = get_rotation_matrix(x_rot, y_rot, z_rot, order=order)

    def set_verbose(self, verbose=True):
        self.verbose = verbose

    def set_absolute_sys_ref(self, x, y, z):
        self.x_o = x
        self.y_o = y
        self.z_o = z
        self.abs_sys_ref = True
        self.T_o = np.array([
            [self.x_o],
            [self.y_o],
            [self.z_o]
        ])

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

    def calculate_transformation_matrix(self):

        # Compute local M
        M_local = np.append(self.R, self.T, axis=1)
        M_local = np.append(M_local, np.array([[0.0, 0.0, 0.0, 1]]), axis=0)

        # If absolute system of reference: i.e., object rotating in itself and rotating as an appendix of another solid
        if self.abs_sys_ref and self.R_static is not None:
            T1 = np.ndarray.flatten(self.T - self.T_o)
            T2 = self.R_static @ T1
            self.translate(T2[0], T2[1], T2[2])
            #
            M_global = np.append(self.R_static, self.T, axis=1)
            M_global = np.append(M_global, np.array([[0.0, 0.0, 0.0, 1]]), axis=0)
            #
            self.M = M_global @ M_local
        else:
            self.M = M_local

        if self.verbose:
            print(
                f"r: {self.get_pos_norm()}, x: {self.x}, y: {self.y}, z: {self.z}, x_rot: {self.x_rot}, y_rot: {self.y_rot}, z_rot: {self.z_rot}")

        # M_global = np.append(self.R_static, self.T, axis=1)
        # M_global = np.append(M_global, np.array([[0.0, 0.0, 0.0, 1]]), axis=0)
        #
        # self.M = M_global @ M_local

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
