from ..shapes.shape import Shape
import numpy as np

class Line(Shape):
	def __init__(self, x = 0, y = 0, z = 0,
					   length = 1, x_rot = 0, 
					   y_rot = 0, z_rot = 0, color = (0, 0, 0), thickness = 1):
		Shape.__init__(self, x, y, z, x_rot, y_rot, z_rot)

		self.name = "LINE"
		self.color = color
		self.color_static = color
		self.grey = (50, 50, 50)
		self.thickness = thickness

		self.shape_points = np.array([
										[0, 0, -length/2],
										[0, 0, length/2]
									])
		self.shape_points_homogeneous = np.append(self.shape_points, np.ones((len(self.shape_points), 1)), axis=1)
