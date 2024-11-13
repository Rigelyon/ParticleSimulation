import os

import cv2
import numpy as np
import pygame
from PIL import Image

from particlesimulation.constants import (
    VIDEO_WIDTH,
    VIDEO_HEIGHT,
)
from particlesimulation.dataclass import UIFlag, GameFlag


class VideoManager:
    def __init__(self):
        self.this_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.this_dir, "assets", "frames")
        self.coords_dir = os.path.join(self.this_dir, "coordinates")
        self.video_path = os.path.join(self.this_dir, "assets", "video.mp4")
        self.audio_path = os.path.join(self.this_dir, "assets", "audio.ogg")

        self.init_capture()

        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music.load(self.audio_path)

        self.frame_count = 0
        self.files_count = len(
            [
                name
                for name in os.listdir(self.coords_dir)
                if os.path.isfile(os.path.join(self.coords_dir, name))
            ]
        )

    def _get_coords(self, image_path):
        image = Image.open(image_path).convert("L")
        pixels = image.load()

        dark_pixels = [
            (y, x)
            for y in range(image.height)
            for x in range(image.width)
            if pixels[x, y] > 50  # White pixels on mode
            # if pixels[x, y] < 50 # Black pixels on mode
            # if 50 < pixels[x, y] < 200 # Outline mode
        ]
        return dark_pixels

    def init_capture(self):
        self.cap = cv2.VideoCapture(self.video_path)
        self.get_fps = self.cap.get(cv2.CAP_PROP_FPS)

    # def calculate_total_progress(self):

    def load_coords(self, frame_number):
        coords_file_name = "ba-" + str(frame_number).zfill(4) + ".npy"
        coords_file_path = os.path.join(self.coords_dir, coords_file_name)
        if os.path.exists(coords_file_path):
            with open(coords_file_path, "rb") as file:
                return np.load(file)
        else:
            print(f"File {coords_file_name} does not exist.")
            return []

    def delete_frames(self):
        if os.path.exists(self.images_dir):
            for file_name in os.listdir(self.images_dir):
                file_path = os.path.join(self.images_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                print(f"Deleted: {file_name}")

    def delete_coords(self):
        if os.path.exists(self.coords_dir):
            for file_name in os.listdir(self.coords_dir):
                file_path = os.path.join(self.coords_dir, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                print(f"Deleted: {file_name}")

    def make_dir(self):
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        elif not os.path.exists(self.coords_dir):
            os.makedirs(self.coords_dir)

    def save_coords(self):
        for frame_count in range(self.frame_count - 1):
            frame_file_name = "ba-" + str(frame_count).zfill(4) + ".jpg"
            frame_file_path = os.path.join(self.images_dir, frame_file_name)
            coords_file_name = frame_file_name[:-4]

            if os.path.exists(frame_file_path):
                dark_pixels_array = self._get_coords(frame_file_path)
                coords_output_file = os.path.join(
                    self.this_dir, "coordinates", f"{coords_file_name}.npy"
                )
                np.save(coords_output_file, dark_pixels_array)

                print(f"Saved coordinates: {coords_file_name}")
            else:
                print(f"File {frame_file_name} doesn't exist")

        self.delete_frames()

    def video_to_images(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized_frame = cv2.resize(gray_frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
            frame_output_name = "ba-" + str(self.frame_count).zfill(4) + ".jpg"
            cv2.imwrite(
                self.images_dir + "/" + frame_output_name,
                resized_frame,
            )
            print(f"Created frames: {frame_output_name}")
            self.frame_count += 1

        self.cap.release()

    def play_mini_player(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(
                frame,
                (
                    round(UIFlag.mini_player_width),
                    round(UIFlag.mini_player_height),
                ),
            )
            video_surf = pygame.image.frombuffer(
                resized_frame.tobytes(), resized_frame.shape[1::-1], "BGR"
            )
            return video_surf

        self.cap.release()

    def loading_operation(self):
        # Delete existing file
        self.delete_frames()
        self.delete_coords()

        GameFlag.video_loading_progress = 0
        self.make_dir()
        self.video_to_images()
        self.save_coords()
