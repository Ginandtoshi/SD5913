import pygame
import numpy as np
import os
import random

# --- CONFIG ---
DATA_FILE = os.path.join('data', 'forest_area.csv') 
TREE_IMG_FILES = [
    os.path.join('assets', 'oak.png'),
    os.path.join('assets', 'birch.png'),
    os.path.join('assets', 'china fir.png'),
    os.path.join('assets', 'yunnan pine.png'),
]
BACKGROUND_IMG_FILE = os.path.join('assets', 'dirt.png')
CURSOR_IMG_FILE = os.path.join('assets', 'cursor.png')
SOUND_FILE = os.path.join('assets', 'button-click.mp3')
SCREEN_SIZE = (1600, 800) 
TREE_VISUAL_RANGE = (2, 10)  # Min/max number of trees to visualize per year

# --- DATA LOADING ---
def load_plantation_data(filepath):
    # Expects CSV with columns: year, amount
    years = []
    areas = []
    try:
        with open(filepath, 'r') as f:
            header = f.readline().strip().split(',')
            year_idx = header.index('Year')
            area_idx = header.index('Forest_Area_sqkm')
            prev_area = None
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    year = int(parts[year_idx])
                    area = int(parts[area_idx])
                    years.append(year)
                    areas.append(area)
    except Exception as e:
        print(f"Error loading data: {e}")
    return years, areas

# --- TREE IMAGE LOADING ---
def load_tree_images(img_files):
    return [pygame.image.load(f).convert_alpha() for f in img_files]

# --- MAPPING FUNCTION ---
def map_tree_amount(amount, min_amount, max_amount, visual_min, visual_max):
    # Map actual amount to visual range
    if max_amount == min_amount:
        return visual_min
    mapped = int(np.interp(amount, [min_amount, max_amount], [visual_min, visual_max]))
    return mapped

# --- MAIN PROGRAM ---
def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Forestry Generative Art')

    # Load assets
    tree_images = load_tree_images(TREE_IMG_FILES)
    # Enlarge dirt.png for better coverage
    raw_bg_img = pygame.image.load(BACKGROUND_IMG_FILE).convert_alpha()
    scale_factor = 1.2  # You can adjust this value for more/less enlargement
    bg_width, bg_height = raw_bg_img.get_width(), raw_bg_img.get_height()
    background_img = pygame.transform.smoothscale(raw_bg_img, (int(bg_width*scale_factor), int(bg_height*scale_factor)))
    cursor_img = pygame.image.load(CURSOR_IMG_FILE).convert_alpha()
    sound = pygame.mixer.Sound(SOUND_FILE)

    # Load data
    years, areas = load_plantation_data(DATA_FILE)
    year_idx = 0
    trees = []

    # UI state
    show_start = True
    show_end = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_start:
                    show_start = False
                elif show_end:
                    # Check if restart button is clicked
                    btn_w, btn_h = 300, 60
                    btn_x, btn_y = SCREEN_SIZE[0]-btn_w-40, SCREEN_SIZE[1]-btn_h-40
                    if btn_x <= event.pos[0] <= btn_x+btn_w and btn_y <= event.pos[1] <= btn_y+btn_h:
                        # Restart program
                        year_idx = 0
                        trees = []
                        show_start = True
                        show_end = False
                elif year_idx < len(years):
                    # Calculate growth for this year
                    if year_idx == 0:
                        growth = 0
                    else:
                        growth = areas[year_idx] - areas[year_idx-1]
                    # Map growth to number of trees
                    tree_count = max(0, int(growth / 3000))
                    # Add new trees for this year (accumulate)
                    for _ in range(tree_count):
                        tree_img = random.choice(tree_images)
                        tree_w, tree_h = tree_img.get_width(), tree_img.get_height()
                        pos = (
                            random.randint(0, SCREEN_SIZE[0] - tree_w),
                            random.randint(0, SCREEN_SIZE[1] - tree_h)
                        )
                        trees.append((tree_img, pos))
                        sound.play()
                    year_idx += 1

        # Fill background with white
        screen.fill((255, 255, 255))
        # Tile the rhombus background image in a brick pattern
        bg_width, bg_height = background_img.get_width(), background_img.get_height()
        overlap_x = int(bg_width * 0.15)  # Horizontal overlap
        overlap_y = int(bg_height * 0.75)  # Vertical overlap (adjust as needed)
        y_offset = -80  # Move tiles up by 40 pixels
        for y in range(y_offset, SCREEN_SIZE[1], bg_height - overlap_y):
            offset_x = (bg_width // 2) if ((y-y_offset) // (bg_height - overlap_y)) % 2 else 0
            for x in range(-offset_x, SCREEN_SIZE[0], bg_width - overlap_x):
                screen.blit(background_img, (x, y))

        if show_start:
            # Draw title, subtitle, and start button
            title_font = pygame.font.SysFont('VCR OSD Mono', 80, bold=True)
            subtitle_font = pygame.font.SysFont('VCR OSD Mono', 40)
            btn_font = pygame.font.SysFont('VCR OSD Mono', 36, bold=True)
            title = title_font.render("Green Growth", True, (0, 120, 0))
            subtitle = subtitle_font.render("China's forestry plantation from 1973 to 2025", True, (0, 80, 0))
            btn_text = btn_font.render("Let's start!", True, (255,255,255))
            # Vertically center title, subtitle, and button
            spacing = 40
            total_height = title.get_height() + spacing + subtitle.get_height() + spacing + 80
            start_y = (SCREEN_SIZE[1] - total_height) // 2
            screen.blit(title, ((SCREEN_SIZE[0]-title.get_width())//2, start_y))
            screen.blit(subtitle, ((SCREEN_SIZE[0]-subtitle.get_width())//2, start_y + title.get_height() + spacing))
            # Draw button
            btn_w, btn_h = 400, 80
            btn_x = (SCREEN_SIZE[0]-btn_w)//2
            btn_y = start_y + title.get_height() + spacing + subtitle.get_height() + spacing
            pygame.draw.rect(screen, (0,120,0), (btn_x, btn_y, btn_w, btn_h), border_radius=20)
            screen.blit(btn_text, (btn_x+(btn_w-btn_text.get_width())//2, btn_y+(btn_h-btn_text.get_height())//2))
        else:
            # Draw trees (accumulated)
            for sprite, pos in trees:
                screen.blit(sprite, pos)
            # Draw custom cursor and bottom text (refresh every frame)
            mx, my = pygame.mouse.get_pos()
            screen.blit(cursor_img, (mx-16, my-16))
            if year_idx > 0 and year_idx <= len(years):
                pixel_font = pygame.font.SysFont('VCR OSD Mono', 36, bold=True)
                text = pixel_font.render(f"Year: {years[year_idx-1]}  Area: {areas[year_idx-1]} sqkm", True, (0, 80, 0))
                screen.blit(text, (20, SCREEN_SIZE[1]-40))
            # Show restart button if at last year
            if year_idx == len(years):
                show_end = True
                btn_font = pygame.font.SysFont('VCR OSD Mono', 32, bold=True)
                btn_text = btn_font.render("Restart the program", True, (255,255,255))
                btn_w, btn_h = btn_text.get_width() + 60, btn_text.get_height() + 30
                btn_x, btn_y = SCREEN_SIZE[0]-btn_w-40, SCREEN_SIZE[1]-btn_h-40
                pygame.draw.rect(screen, (0,120,0), (btn_x, btn_y, btn_w, btn_h), border_radius=20)
                screen.blit(btn_text, (btn_x+(btn_w-btn_text.get_width())//2, btn_y+(btn_h-btn_text.get_height())//2))
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
