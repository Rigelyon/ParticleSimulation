import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 600, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sakura Petal Falling Animation")
clock = pygame.time.Clock()


# Define the Petal class
class Petal:
    def __init__(self):  # Corrected the method name here
        # Set random starting position at the top of the screen
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-100, -10)
        self.size = random.uniform(10, 20)
        self.angle = random.randint(80, 100)  # Angle of the petal fall
        self.fall_speed = random.uniform(2, 5)
        self.wind_direction = random.uniform(-1, 1)  # Horizontal drift from wind
        self.color = (255, 182, 193)  # Pink color for the petal

        # Create a surface for the petal shape (circle shaped petal)
        self.image = pygame.Surface(
            (self.size * 2, self.size), pygame.SRCALPHA
        )  # Use SRCALPHA for transparency
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color
        pygame.draw.polygon(
            self.image,
            self.color,
            [(self.size * 1.0, 0), (self.size * 2.0, self.size), (0, self.size)],
        )
        self.image = pygame.transform.rotate(
            self.image, random.uniform(-30, 30)
        )  # Rotate slightly for randomness
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def fall(self):
        # Move the petal downward and apply horizontal wind drift
        self.rect.y += self.fall_speed
        self.rect.x += self.wind_direction

        # Reset position if petal goes below the screen
        if self.rect.y > screen_height:
            self.rect.y = random.randint(-100, -10)
            self.rect.x = random.randint(0, screen_width)
            self.fall_speed = random.uniform(2, 5)
            self.wind_direction = random.uniform(-1, 1)


# Create a list of petals
petals = [Petal() for _ in range(40)]  # More petals for a denser effect

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Set the background to black

    for petal in petals:
        petal.fall()  # Update the position of each petal
        screen.blit(petal.image, petal.rect)  # Draw each petal on the screen

    pygame.display.flip()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)  # Control the frame rate to 60 FPS

pygame.quit()
