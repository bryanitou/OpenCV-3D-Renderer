import cv2
import numpy as np
import copy

class Draw:
    def __init__(self, width, height, save_as_video=False, window_name="Canvas"):
        self.width = width
        self.height = height
        img_bck = cv2.imread('backgrounds/earth2.jpeg')
        imb_bck_resized = cv2.resize(img_bck, (height, width), interpolation = cv2.INTER_AREA)
        self.image_background = imb_bck_resized
        self.canvas = 255 * np.ones((height, width, 3)).astype("uint8")
        self.window_name = window_name
        self.save_as_video = save_as_video

        if self.save_as_video:
            self.video_writer = cv2.VideoWriter('out/output.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 30.0,
                                                (self.width, self.height))

    def clear(self):
        # self.canvas = 255 * np.ones((self.height, self.width, 3)).astype("uint8")
        self.canvas = copy.deepcopy(self.image_background)

    def draw(self, pts, obj, draw_points=False):
        if draw_points:
            for pt in pts:
                cv2.circle(self.canvas, pt, 3, (0, 255, 0), -1)

        if obj.name == "CUBE":
            for i in range(3):
                cv2.line(self.canvas, pts[i, :], pts[i + 1, :], obj.color, obj.thickness)
                cv2.line(self.canvas, pts[i, :], pts[i + 4, :], obj.color, obj.thickness)
                cv2.line(self.canvas, pts[i + 4, :], pts[i + 4 + 1, :], obj.color, obj.thickness)
                if i == 2:
                    cv2.line(self.canvas, pts[i + 1, :], pts[0, :], obj.color, obj.thickness)
                    cv2.line(self.canvas, pts[i + 1, :], pts[7, :], obj.color, obj.thickness)
                    cv2.line(self.canvas, pts[i + 4 + 1, :], pts[4, :], obj.color, obj.thickness)

        if obj.name == "RECTANGLE":
            for i in range(3):
                cv2.line(self.canvas, pts[i, :], pts[i + 1, :], obj.color, obj.thickness)
            cv2.line(self.canvas, pts[0, :], pts[-1, :], obj.color, obj.thickness)

        if obj.name == "SPHERE":
            for i in range(360 // obj.resolution):
                offset = i * 360 // obj.resolution
                offset_next = (i + 1) * 360 // obj.resolution
                for j in range(360 // obj.resolution - 1):
                    cv2.line(self.canvas, pts[offset + j, :], pts[offset + j + 1, :], obj.color, obj.thickness)
                    if i < 360 // obj.resolution - 1:
                        cv2.line(self.canvas, pts[offset + j, :], pts[offset_next + j, :], obj.color, obj.thickness)
                cv2.line(self.canvas, pts[offset + j + 1, :], pts[offset + 0, :], obj.color, obj.thickness)

        if obj.name == "TORUS":
            for i in range(360 // obj.resolution):
                offset = i * 360 // obj.resolution
                offset_next = (i + 1) * 360 // obj.resolution
                for j in range(360 // obj.resolution - 1):
                    cv2.line(self.canvas, pts[offset + j, :], pts[offset + j + 1, :], obj.color, obj.thickness)

                    if i < 360 // obj.resolution - 1:
                        cv2.line(self.canvas, pts[offset + j, :], pts[offset_next + j, :], obj.color, obj.thickness)

                    else:
                        cv2.line(self.canvas, pts[offset + j, :], pts[0 + j, :], obj.color, obj.thickness)

                cv2.line(self.canvas, pts[offset + j + 1, :], pts[offset + 0, :], obj.color, obj.thickness)

        if obj.name == "3D File":
            for i in range(len(pts) - 1):
                cv2.line(self.canvas, pts[i, :], pts[i + 1, :], obj.color, obj.thickness)

        if obj.name == "LINE":
            cv2.line(self.canvas, pts[0, :], pts[1, :], obj.color, obj.thickness)

        if obj.name == "SceneCursor":
            pass

    def show(self):
        # self.canvas[self.image_background.shape[0], self.image_background.shape[1]] = self.image_background

        cv2.imshow(self.window_name, self.canvas)
        if self.save_as_video:
            self.video_writer.write(self.canvas)
        return cv2.waitKey(1)

    def destroy_scene(self):
        if self.save_as_video:
            self.video_writer.release()

        cv2.destroyAllWindows()
