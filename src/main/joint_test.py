from src.cvrenderer.shapes.line import Line
from src.cvrenderer.scene import Scene
from src.cvrenderer.camera import Camera
from src.cvrenderer.shapes.joint import Joint

object_1 = Line(x = 0, y = 0, z = 0.5, length = 1, thickness=2, color=(255, 0, 0))
object_2 = Line(x = 0, y = 0, z = -0.5, length = 1, thickness=2, color=(0, 255, 0))

joint = Joint(x = 0.0, y = 0.0, z = 0.0, axis = [0, 1, 0], parent = object_1, child = object_2)

scene_width = 700
scene_height = 700

scene = Scene(width = scene_width, height = scene_height, save_as_video = False)


camera = Camera(x = 0, y = 0, z = 20,
				cx = scene_width//2, cy = scene_height//2, 
				width = scene_width, height = scene_height,
				x_rot = 0, z_rot = 0,
				fov_x = 60, fov_y = 60)

scene.add_object(object_1)
scene.add_object(object_2)
scene.add_object(joint)
# scene.add_axis(scaler=1)

scene.add_camera(camera)

ang = 0
while True:
	k = scene.render_scene()
	object_2.rotate(ang, ang, ang)
	object_1.rotate(ang, ang, ang)
	# joint.rotate(ang, ang, ang)
	ang += 0.025
	if k == ord("q"):
		break

scene.destroy_scene()
