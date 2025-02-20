from src.cvrenderer.shapes.cube import Cube
from src.cvrenderer.shapes.sphere import Sphere
from src.cvrenderer.shapes.torus import Torus

from src.cvrenderer.scene import Scene
from src.cvrenderer.camera import Camera

import numpy as np


def main():
    scene_width = 700
    scene_height = 700

    scene = Scene(width=scene_width, height=scene_height, save_as_video=False)

    camera = Camera(x=0, y=0, z=20,
                    cx=scene_width // 2, cy=scene_height // 2,
                    width=scene_width, height=scene_height,
                    x_rot=np.pi / 6, z_rot=4 * np.pi / 3,
                    fov_x=60, fov_y=60)
    cube = Cube(x=3)
    sphere = Sphere(y=3)
    torus = Torus(z=2, x=-3, y=-3, x_rot=np.pi / 2)

    scene.add_object(cube)
    scene.add_object(sphere)
    scene.add_object(torus)
    scene.add_axis(scaler=1)

    scene.add_camera(camera)

    ang = 0
    while True:
        # scene.move_axis(delta_x = 0.01, delta_y = -0.01)
        camera.rotate(np.pi/6, 0, ang)
        sphere.rotate(ang, ang, 0)
        cube.rotate(ang, ang, ang)
        cube.translate(0, 0, 3 + np.sin(ang))
        torus.rotate(x_rot=np.pi / 2, y_rot=ang * 2, z_rot=0)
        k = scene.render_scene()
        ang += 0.025
        if k == ord("q"):
            break

    scene.destroy_scene()


# Script entry point
if __name__ == '__main__':
    main()
