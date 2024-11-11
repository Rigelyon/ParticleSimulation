import json
import os

import cv2
import pygame
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
        self.video_path = os.path.join(self.script_dir, "assets", "video.mp4")
        self.audio_path = os.path.join(self.script_dir, "assets", "audio.ogg")
        self.cap = cv2.VideoCapture(self.video_path)

        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music.load(self.audio_path)

        self.frame_count = 0
        self.files_count = len(
            [
                name
                for name in os.listdir(self.images_dir)
                if os.path.isfile(os.path.join(self.images_dir, name))
            ]
        )

    def _get_coords(self, image_path):
        image = Image.open(image_path).convert("L")
        pixels = image.load()

        dark_pixels = [
            (y, x)
            for y in range(image.height)
            for x in range(image.width)
            if pixels[x, y] > 100
        ]

        return dark_pixels

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

    def save_coords(self):
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

    def video_to_images(self):
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
