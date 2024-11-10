from random import sample

from particlesimulation.video_manager import VideoManager

video = VideoManager()
dark = video.load_coords(0)
print(sample(dark, 10))
