import pygame
import pandas as pd
import sys

# Load tide data from CSV
data = pd.read_csv('tides_processed.csv')
tide_levels = data['tide_level'].astype(float).tolist()

# Pygame setup
WIDTH, HEIGHT = 800, 400
FPS = 60
WAVE_COLOR = (80, 180, 255)  # Light-middle blue
BG_COLOR = (30, 30, 30)
POINT_RADIUS = 2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tide Level Wave Animation')
clock = pygame.time.Clock()

# Scale tide levels to fit the screen vertically
tide_min, tide_max = min(tide_levels), max(tide_levels)
def scale_y(val):
    return HEIGHT - int((val - tide_min) / (tide_max - tide_min) * (HEIGHT - 40))

# Animation variables
wave_length = min(len(tide_levels), WIDTH)
start_idx = 0
import random
speed = random.randint(1, 100)  # random speed between 1 and 100
print(f"Wave speed: {speed} pixels/frame")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    # Draw the wave
    points = []
    for i in range(wave_length):
        x = i
        idx = (start_idx + i) % len(tide_levels)
        y = scale_y(tide_levels[idx])
        points.append((x, y))
    if len(points) > 1:
        pygame.draw.lines(screen, WAVE_COLOR, False, points, 2)
    for pt in points:
        pygame.draw.circle(screen, WAVE_COLOR, pt, POINT_RADIUS)

    pygame.display.flip()
    clock.tick(FPS)
    start_idx = (start_idx + speed) % len(tide_levels)

pygame.quit()
sys.exit()
