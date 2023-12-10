import os
import time

from src.cvrenderer.shapes.cube import Cube
from src.cvrenderer.shapes.line import Line
from src.cvrenderer.shapes.sphere import Sphere
from src.cvrenderer.shapes.torus import Torus

from src.cvrenderer.scene import Scene
from src.cvrenderer.camera import Camera

import numpy as np

# Import CSV stuff
import csv


def write_csv(f, row):
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerow(row)


def open_csv() -> csv.writer:
    path = "out/track.csv"

    if os.path.exists(path):
        os.remove(path)

    # open the file in the append mode
    f = open(path, 'a')

    return f


def main():
    # Open tracking file
    f = open_csv()
    write_csv(f, ["i", "x_body", "y_body", "z_body", "x_panel", "y_panel", "z_panel",
                  "att1_body", "att2_body", "att3_body", "att1_panel_right", "att2_panel_right", "att3_panel_right"])

    # Set scene width
    scene_width = 700
    scene_height = 700

    # Rotation being done
    ang_body_dt = np.array([0.0025, 0.0025, 0.0025]) * 3

    # Scene
    scene = Scene(width=scene_width, height=scene_height, save_as_video=True)

    # Set camera
    camera = Camera(x=0, y=0, z=20, cx=scene_width // 2, cy=scene_height // 2,
                    width=scene_width, height=scene_height,
                    x_rot=np.pi / 6, z_rot=4 * np.pi / 3,
                    fov_x=60, fov_y=60)

    # Set geometric figures
    body = Cube(x=0, y=0, z=0, w=3, h=1, l=1, color=(10, 10, 180), thickness=2)
    panel_right = Cube(x=0, y=1, z=0, w=2, h=1, l=0.1, x_rot=0.0, y_rot=0.0, z_rot=0.0, color=(0, 0, 255), thickness=2)
    panel_left = Cube(x=0.0, y=-1, z=0, w=2, h=1, l=0.1, x_rot=0.0, y_rot=0.0, z_rot=0.0, color=(0, 0, 255), thickness=2)
    # panel_right_center_sphere = Sphere(x=panel_right.x, y=panel_right.y, z=panel_right.z, radius=0.1, color=(50, 190, 50))

    # Set static in parent
    body.set_R_static(*ang_body_dt)
    # panel_right.move_center(0.0, 1.0, 0.0) # TODO: This works
    # panel_right.translate(0.0, 0.5, 0.0)
    # panel_left.move_center(0.0, -1.0, 0.0) # TODO: This works
    # panel_left.translate(0.0, -0.5, 0.0)

    # Set verbose
    panel_right.set_verbose(True)

    scene.add_object(body)
    scene.add_object(panel_right)
    scene.add_object(panel_left)
    # scene.add_object(panel_right_center_sphere)
    scene.add_axis(scaler=1.0)

    scene.add_camera(camera)
    zero_array = np.array([0.0, 0.0, 0.0])
    body_sgn = np.array([1.0, 1.0, 1.0])
    left_sgn = np.array([1.0, 1.0, 1.0])
    right_sgn = np.array([1.0, 1.0, 1.0])
    line_sgn = np.array([1.0, 1.0, 1.0])
    body_ang0 = np.array([0.0, 0.0, 0.0])
    left_ang0 = np.array([0.0, 0.0, 0.0])
    line_ang0 = np.array([np.pi / 2, 0.0, 0.0])
    right_ang0 = np.array([0.0, 0.0, 0.0])

    # Starting attitude of body
    ang_body = np.array([0.0, 0.0, 0.0])

    # Starting attitude of panels
    ang_panels = np.array([0.0, 0.0, 0.0])
    ang_panels_dt = np.array([0.0, 0.01, 0.0])
    ang_panels_dt_sign = 1

    ang_cam = 0
    idx = 0
    while True:
        k = scene.render_scene()

        scene.move_axis(delta_x = 0.01, delta_y = -0.01)
        # camera.rotate(np.pi / 6, 0, ang_cam)
        body.rotate(*(ang_body * body_sgn + body_ang0))

        # Attach movement to parent
        panel_right.attach_parent(body)
        panel_left.attach_parent(body)

        # Move the panels standalone
        panel_right.rotate(*(ang_panels * right_sgn + right_ang0))
        panel_left.rotate(*(ang_panels * left_sgn + left_ang0))

        # Centers
        # panel_right_center_sphere.translate(x=panel_right.x, y=panel_right.y, z=panel_right.z)

        # Body movement
        ang_body += ang_body_dt

        # Panels movement
        ang_panels += ang_panels_dt*ang_panels_dt_sign

        # Panels movement
        if idx % 100 == 0:
            ang_panels_dt_sign = ang_panels_dt_sign * -1

        # Camera movement
        ang_cam += 0.0025

        idx += 1
        if k == ord("q"):
            break

        # Write in csv
        if idx < 6000:
            write_csv(f, [idx, *np.ndarray.flatten(body.T), *np.ndarray.flatten(panel_right.T),
                          body.x_rot, body.y_rot, body.z_rot, panel_right.x_rot, panel_right.y_rot, panel_right.z_rot])

    scene.destroy_scene()

    # close the file
    f.close()


# Script entry point
if __name__ == '__main__':
    main()
