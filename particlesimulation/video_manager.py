import os
import shutil

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
        self.images_dir = os.path.join(self.this_dir, "assets", "images")
        self.coords_file_dir = os.path.join(self.this_dir, "coordinates")
        self.video_path = os.path.join(self.this_dir, "assets", "video.mp4")
        self.audio_path = os.path.join(self.this_dir, "assets", "audio.ogg")

        self.init_capture()

        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.music.load(self.audio_path)

        self.make_dir()

        self.frame_count = 0
        self.coords_files_count = len(
            [
                name
                for name in os.listdir(self.coords_file_dir)
                if os.path.isfile(os.path.join(self.coords_file_dir, name))
            ]
        )

    def _get_coords(self, image_path):
        image = Image.open(image_path).convert("L")
        pixels = image.load()

        dark_pixels = [
            (y, x)
            for y in range(image.height)
            for x in range(image.width)
            if pixels[x, y] > 50  # White pixels mode
            # if pixels[x, y] < 50 # Black pixels mode
            # if 50 < pixels[x, y] < 200 # Outline mode
        ]
        return dark_pixels

    def init_capture(self):
        self.cap = cv2.VideoCapture(self.video_path)
        self.get_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.get_max_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def calculate_total_progress(self):
        images_count = len(
            [
                name
                for name in os.listdir(self.images_dir)
                if os.path.isfile(os.path.join(self.images_dir, name))
            ]
        )
        coords_file_count = len(
            [
                name
                for name in os.listdir(self.coords_file_dir)
                if os.path.isfile(os.path.join(self.coords_file_dir, name))
            ]
        )
        total_percentages = (images_count + coords_file_count) / (
            2 * self.get_max_frames
        )
        return total_percentages

    def load_coords(self, image_number):
        coords_file_name = "ba-" + str(image_number).zfill(4) + ".npy"
        coords_file_path = os.path.join(self.coords_file_dir, coords_file_name)
        if os.path.exists(coords_file_path):
            with open(coords_file_path, "rb") as file:
                return np.load(file)
        else:
            print(f"File {coords_file_name} does not exist.")
            return []

    def delete_images_contents(self):
        if os.path.exists(self.images_dir):
            for filename in os.listdir(self.images_dir):
                image_path = os.path.join(self.images_dir, filename)
                try:
                    if os.path.isfile(image_path) or os.path.islink(image_path):
                        os.unlink(image_path)
                    elif os.path.isdir(image_path):
                        shutil.rmtree(image_path)
                except Exception as e:
                    print(f"Failed to delete {image_path}: {e}")

    def delete_coords_contents(self):
        if os.path.exists(self.coords_file_dir):
            for filename in os.listdir(self.coords_file_dir):
                coord_file_path = os.path.join(self.coords_file_dir, filename)
                try:
                    if os.path.isfile(coord_file_path) or os.path.islink(
                        coord_file_path
                    ):
                        os.unlink(coord_file_path)  # Remove file or symbolic link
                    elif os.path.isdir(coord_file_path):
                        shutil.rmtree(coord_file_path)
                except Exception as e:
                    print(f"Failed to delete {coord_file_path}: {e}")

    def make_dir(self):
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        if not os.path.exists(self.coords_file_dir):
            os.makedirs(self.coords_file_dir)

    def images_to_array_coordinates(self):
        print("Starting to load images to array of coordinates..")
        for frame_count in range(self.frame_count - 1):
            if not GameFlag.is_video_loading_in_progress:
                break

            image_file_name = "ba-" + str(frame_count).zfill(4) + ".jpg"
            image_file_path = os.path.join(self.images_dir, image_file_name)
            coords_file_name = image_file_name[:-4]

            if os.path.exists(image_file_path):
                dark_pixels_array = self._get_coords(image_file_path)
                coords_output_file = os.path.join(
                    self.this_dir, "coordinates", f"{coords_file_name}.npy"
                )
                np.save(coords_output_file, dark_pixels_array)

                # print(f"Coordinates loaded: {coords_file_name}")
            else:
                print(f"File {image_file_name} doesn't exist")
        self.delete_images_contents()

    def video_to_images(self):
        print("Starting to load video to images..")
        while self.cap.isOpened():
            if not GameFlag.is_video_loading_in_progress:
                break

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
            # print(f"Frames created: {frame_output_name}")
            self.frame_count += 1

        self.cap.release()

    def play_mini_player(self):
        frame_index = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if not GameFlag.is_video_running:
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
            frame_index += 1
            return video_surf

        self.cap.release()

    def stop_loading_operation(self):
        GameFlag.is_video_loading_in_progress = False
        self.frame_count = 0

    def start_loading_operation(self):
        GameFlag.is_video_loading_in_progress = True
        self.delete_images_contents()
        self.delete_coords_contents()

        GameFlag.video_loading_progress = 0
        self.make_dir()
        self.init_capture()
        self.video_to_images()
        self.images_to_array_coordinates()
