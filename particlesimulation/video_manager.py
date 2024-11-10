import json
import os

import cv2
import numpy as np
from PIL import Image

from particlesimulation.constants import (
    VIDEO_WIDTH,
    VIDEO_HEIGHT,
)


class VideoManager:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.script_dir, "assets", "frames")
        self.coordinates_dir = os.path.join(self.script_dir, "coordinates")
        video_path = os.path.join(self.script_dir, "assets", "video.mp4")
        self.cap = cv2.VideoCapture(video_path)

        self.frame_count = 0

    def _get_coords(self, image_path):
        image = Image.open(image_path)
        np_image = np.array(image)
        dark_pixels = np.argwhere(np_image < 50)

        return dark_pixels.tolist()

    def load_coords(self, frame_number):
        file_name = "ba-" + str(frame_number).zfill(4) + ".json"
        file_path = os.path.join(self.coordinates_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                return json.load(json_file)
        else:
            print(f"File {file_name} does not exist.")
            return []

    def delete_existing_frames(self):
        if os.path.exists(self.images_dir):
            for file_name in os.listdir(self.images_dir):
                file_path = os.path.join(self.images_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                print(f"Deleting existing frames: {file_name}")

    def make_dir(self):
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        elif not os.path.exists(self.coordinates_dir):
            os.makedirs(self.coordinates_dir)

    def process_coords(self):
        for frame_count in range(self.frame_count - 1):
            file_name = "ba-" + str(frame_count).zfill(4) + ".jpg"
            file_path = os.path.join(self.images_dir, file_name)

            if os.path.exists(file_path):
                dark_pixels = self._get_coords(file_path)
                output_file = os.path.join(
                    self.script_dir, "coordinates", f"{file_name[:-4]}.json"
                )
                with open(output_file, "w") as json_file:
                    json.dump(dark_pixels, json_file)

                print(f"Coordinates saved to {output_file}")
            else:
                print(f"File {file_name} doesn't exist")

    def process_frames(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_frame = cv2.resize(gray_frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            file_name = "ba-" + str(self.frame_count).zfill(4) + ".jpg"
            cv2.imwrite(
                self.images_dir + "/" + file_name,
                resized_frame,
            )
            print(f"Created frames: {file_name}")
            self.frame_count += 1

        self.cap.release()
