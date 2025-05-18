# Particle Simulation

A customizable particle simulation engine built with Pygame.

## Features

- **Particle Types**:
    - Circle
    - Snow
    - Leaves
    - Steam
    - Firefly
    - Rain
    - Sakura
    - Vortex

- **Customizable Properties**:
    - Color selection via color picker
    - Particle size (min/max)
    - Movement speed (min/max)
    - Fade speed (min/max)
    - Particle multiplier for density control

- **Animation Sequence Mode**:
    - Process video files to create particle animations
    - Convert video frames to particle coordinates
    - Synchronized audio playback
    - Mini player display during playback

## Controls

- **Space Bar**: Toggle video playback (first time will load the video before playing)
- **C Key**: Clear all particles
- **Mouse Click**: Remove particles at cursor position

## Screenshots
- Bad Apple Animation
  ![Bad Apple Animation](/screenshots/bad_apple_particle_screenshot.png)
- Circle Particle
  ![Circle Particle](/screenshots/circle_particle_screenshot.png)
- Firefly Particle
  ![Firefly Particle](/screenshots/firefly_particle_screenshot.png)
- Leaves Particle
  ![Leaves Particle](/screenshots/leaves_particle_screenshot.png)
- Rain Particle
  ![Rain Particle](/screenshots/rain_particle_screenshot.png)
- Sakura Particle
  ![Sakura Particle](/screenshots/sakura_particle_screenshot.png)
- Snow Particle
  ![Snow Particle](/screenshots/snow_particle_screenshot.png)
- Steam Particle
  ![Steam Particle](/screenshots/steam_particle_screenshot.png)
- Vortex Particle
  ![Vortex Particle](/screenshots/vortex_particle_screenshot.png)

## How Video Processing Works

1. When you first load a video:
    - The application extracts frames from the video
    - Each frame is converted to grayscale and resized
    - Frames are saved as images in the `assets/images/` directory
    - Image pixels are analyzed to extract coordinate data
    - Coordinate data is saved in the `coordinates/` directory as NumPy files

2. During video playback:
    - The application loads coordinate data from files
    - Coordinates are used to position particles on screen
    - Audio is synchronized with particle animations
    - A mini player shows the original video in the corner

> I know this might sounds ineffecient and performance heavy (it is). But i don't really care because this was made when i still learning how to code. In fact, i'm quite proud with how it turned out

## Installation

1. Clone this repository:
```
git clone https://github.com/Rigelyon/ParticleSimulation.git
cd ParticleSimulation
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

## Contributing

Feel free to contribute by creating a pull request

## License

This project is licensed under the [MIT License](LICENSE)