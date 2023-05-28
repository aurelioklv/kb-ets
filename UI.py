import pygame
import sys
import time
import subprocess

pygame.init()

# Define screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Define types box size and position
TYPES_BOX_WIDTH = 124
TYPES_BOX_HEIGHT = 287
TYPES_BOX_X = 78
TYPES_BOX_Y = 299

# Define cluster box size and position
CLUSTER_BOX_WIDTH = 124
CLUSTER_BOX_HEIGHT = 287
CLUSTER_BOX_X = 231
CLUSTER_BOX_Y = 299

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Map Region Randomizer")
clock = pygame.time.Clock()

# Define colors
BG = (224, 251, 252)
WHITE = (255, 255, 255)
BLUEL = (152, 193, 217)
BLUED = (61,90,128)
ORANGE = (238,108,77)
BLACK = (0,0,0)

# Define button properties
button_width = 324
button_height = 56
button_x = 59
button_y = 633

# Define button state
button1_clicked = False

# Define font
font_size = 18
font = pygame.font.Font('Poppins-Medium.ttf', font_size)
font_med = pygame.font.Font('Poppins-Medium.ttf', 26)
font_semi = pygame.font.Font('Poppins-SemiBold.ttf', 40)
font_semiB = pygame.font.Font('Poppins-SemiBold.ttf', 32)
font_bold= pygame.font.Font('Poppins-Bold.ttf', 20)

# Create empty list for lines of text
cluster_box_lines = [""]
types_box_lines = [""]
current_cluster_box_line = 0
current_types_box_line = 0

# For outputting text onto the screen
txt_title = font_semi.render("MAP REGION RANDOMIZER", True, WHITE)
txt_titleO = font_semi.render("MAP REGION RANDOMIZER", True, ORANGE)
title_pos = txt_title.get_rect(center=(488 + 631.21/2,32 + 80/2))
title_posO = txt_title.get_rect(center=(492 + 631.21/2,32 + 80/2))
txt_types = font_med.render("Types :", True, WHITE)
txt_cluster = font_med.render("Cluster :", True, WHITE)
txt_info = font_semiB.render("INFORMATION", True, WHITE)
txt_infoO = font_semiB.render("INFORMATION", True, ORANGE)
txt_info1 = font.render("Input for the cluster type :", True, WHITE)
txt_info2 = font.render("entry : Single node", True, WHITE)
txt_info3 = font.render("long : 3 node long", True, WHITE)
txt_info4 = font.render("3x3 : 9 node 3x3", True, WHITE)
txt_color = font_semiB.render("Color", True, WHITE)
txt_colorO = font_semiB.render("Color", True, ORANGE)
txt_color0 = font_semiB.render("Guide", True, WHITE)
txt_color0O = font_semiB.render("Guide", True, ORANGE)
txt_color1 = font.render("3x3 :                            long : ", True, WHITE)
txt_color2 = font.render("- Clearing                   - Road", True, WHITE)
txt_color3 = font.render("- Forest                       - River", True, WHITE)
txt_color4 = font.render("- Camp                       - Ravine", True, WHITE)
txt_color5 = font.render("- Lake", True, WHITE)



# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def save_text_to_file(lines, filename):
    text = "\n".join(lines) 
    with open(filename, 'w') as file:
        file.write(text)

def render_and_show_solution():
    if types_box_lines:
        save_text_to_file(types_box_lines, "types.txt")
        print("Teks telah disimpan dalam file", "types.txt")
    if cluster_box_lines:
        save_text_to_file(cluster_box_lines, "clusters.txt")
        print("Teks telah disimpan dalam file", "clusters.txt")
    subprocess.call(["python", "main.py"])
    # time.sleep(5)
    imp = pygame.image.load("D:\kb_ets\solution.png")
    screen.blit(imp, (551, 126))

# Game loop
run = True
cluster_box_cursor_visible = True
types_box_cursor_visible = True
cluster_box_cursor_timer = time.time()
types_box_cursor_timer = time.time()
active_box = "types"  # Initially set active box to types

# Output background & text template
screen.fill(BG)
pygame.draw.rect(screen, BLUEL, pygame.Rect(492,32,631.21,80), 0, 19)
pygame.draw.rect(screen, BLUED, pygame.Rect(492,32,631.21,80), 5, 19)

pygame.draw.rect(screen, BLUEL, pygame.Rect(51,41,341,183), 0, 41)
pygame.draw.rect(screen, BLUED, pygame.Rect(51,41,341,183), 5, 41)

pygame.draw.rect(screen, BLUEL, pygame.Rect(485,529,647,160), 0, 19)
pygame.draw.rect(screen, BLUED, pygame.Rect(485,529,647,160), 5, 19)

screen.blit(txt_titleO, title_posO)
screen.blit(txt_title, title_pos)

screen.blit(txt_infoO, (110,45))
screen.blit(txt_info, (106,45))
screen.blit(txt_info1, (100,104))
screen.blit(txt_info2, (140,129))
screen.blit(txt_info3, (140,154))
screen.blit(txt_info4, (153,183))

screen.blit(txt_colorO, (527,574))
screen.blit(txt_color, (523,574))
screen.blit(txt_color0O, (523,610))
screen.blit(txt_color0, (520,610))
screen.blit(txt_color1, (665,540))
screen.blit(txt_color2, (665,572))
screen.blit(txt_color3, (665,599))
screen.blit(txt_color4, (665,624))
screen.blit(txt_color5, (665,652))

pygame.draw.rect(screen, (173,255,47), pygame.Rect(779,576,15,15))
pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(779,605,15,15))
pygame.draw.rect(screen, ORANGE, pygame.Rect(779,633,15,15))
pygame.draw.rect(screen, (65,104,225), pygame.Rect(779,661,15,15))

pygame.draw.rect(screen, (218, 165, 32), pygame.Rect(998,573,15,15))
pygame.draw.rect(screen, (135, 206, 235), pygame.Rect(998,602,15,15))
pygame.draw.rect(screen, (192,192,192), pygame.Rect(998,630,15,15))

while run:
    #update background
    pygame.draw.rect(screen, BLUEL, pygame.Rect(51,250, 333, 355), 0, 41)
    pygame.draw.rect(screen, BLUED, pygame.Rect(51,250, 333, 355), 5, 41)

    pygame.draw.rect(screen, ORANGE, pygame.Rect(TYPES_BOX_X,TYPES_BOX_Y,TYPES_BOX_WIDTH,TYPES_BOX_HEIGHT), 5, 15)
    screen.blit(txt_types, (90, 260))

    pygame.draw.rect(screen, ORANGE, pygame.Rect(CLUSTER_BOX_X,CLUSTER_BOX_Y,CLUSTER_BOX_WIDTH,CLUSTER_BOX_HEIGHT), 5, 15)
    screen.blit(txt_cluster, (235,262))

    # Display typed input in the cluster box
    for i, line in enumerate(cluster_box_lines):
        draw_text(line, font, WHITE, CLUSTER_BOX_X + 15, CLUSTER_BOX_Y + 5 + (i * font_size))

    # Display typed input in the types box
    for i, line in enumerate(types_box_lines):
        draw_text(line, font, WHITE, TYPES_BOX_X + 15, TYPES_BOX_Y + 5 + (i * font_size))

    # Draw blinking cursor in the cluster box
    if active_box == "cluster":
        if time.time() - cluster_box_cursor_timer >= 0.5:
            cluster_box_cursor_visible = not cluster_box_cursor_visible
            cluster_box_cursor_timer = time.time()

        if cluster_box_cursor_visible:
            cursor_pos = font.size(cluster_box_lines[current_cluster_box_line])[0] + CLUSTER_BOX_X + 15
            cursor_y = CLUSTER_BOX_Y + 5 + (current_cluster_box_line * font_size)
            pygame.draw.line(screen, ORANGE, (cursor_pos, cursor_y), (cursor_pos, cursor_y + font_size), 2)

    # Draw blinking cursor in the types box
    if active_box == "types":
        if time.time() - types_box_cursor_timer >= 0.5:
            types_box_cursor_visible = not types_box_cursor_visible
            types_box_cursor_timer = time.time()

        if types_box_cursor_visible:
            cursor_pos = font.size(types_box_lines[current_types_box_line])[0] + TYPES_BOX_X + 15
            cursor_y = TYPES_BOX_Y + 5 + (current_types_box_line * font_size)
            pygame.draw.line(screen, ORANGE, (cursor_pos, cursor_y), (cursor_pos, cursor_y + font_size), 2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if event.button == 1:  # Left mouse button
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    button1_clicked = True
                    render_and_show_solution()

            # Check if the cluster box is clicked
            if CLUSTER_BOX_X <= mouse_pos[0] <= CLUSTER_BOX_X + CLUSTER_BOX_WIDTH and CLUSTER_BOX_Y <= mouse_pos[1] <= CLUSTER_BOX_Y + CLUSTER_BOX_HEIGHT:
                active_box = "cluster"
            # Check if the types box is clicked
            elif TYPES_BOX_X <= mouse_pos[0] <= TYPES_BOX_X + TYPES_BOX_WIDTH and TYPES_BOX_Y <= mouse_pos[1] <= TYPES_BOX_Y + TYPES_BOX_HEIGHT:
                active_box = "types"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if active_box == "cluster":
                    if current_cluster_box_line >= 0 and len(cluster_box_lines[current_cluster_box_line]) > 0:
                        cluster_box_lines[current_cluster_box_line] = cluster_box_lines[current_cluster_box_line][:-1]
                    elif current_cluster_box_line > 0 and len(cluster_box_lines[current_cluster_box_line]) == 0:
                        cluster_box_lines.pop(current_cluster_box_line)
                        current_cluster_box_line -= 1
                elif active_box == "types":
                    if current_types_box_line >= 0 and len(types_box_lines[current_types_box_line]) > 0:
                        types_box_lines[current_types_box_line] = types_box_lines[current_types_box_line][:-1]
                    elif current_types_box_line > 0 and len(types_box_lines[current_types_box_line]) == 0:
                        types_box_lines.pop(current_types_box_line)
                        current_types_box_line -= 1

            elif event.key == pygame.K_RETURN:
                if active_box == "cluster" and cluster_box_cursor_visible and cursor_y + font_size < CLUSTER_BOX_Y + CLUSTER_BOX_HEIGHT - font_size:
                    cluster_box_lines.insert(current_cluster_box_line + 1, "")
                    current_cluster_box_line += 1
                elif active_box == "types" and types_box_cursor_visible and cursor_y + font_size < TYPES_BOX_Y + TYPES_BOX_HEIGHT - font_size:
                    types_box_lines.insert(current_types_box_line + 1, "")
                    current_types_box_line += 1

            elif event.key == pygame.K_UP:
                if active_box == "cluster" and current_cluster_box_line > 0 and cluster_box_cursor_visible:
                    current_cluster_box_line -= 1
                elif active_box == "types" and current_types_box_line > 0 and types_box_cursor_visible:
                    current_types_box_line -= 1

            elif event.key == pygame.K_DOWN:
                if active_box == "cluster" and current_cluster_box_line < len(cluster_box_lines) - 1 and cluster_box_cursor_visible:
                    current_cluster_box_line += 1
                elif active_box == "types" and current_types_box_line < len(types_box_lines) - 1 and types_box_cursor_visible:
                    current_types_box_line += 1

            else:
                if active_box == "cluster" and cluster_box_cursor_visible and cursor_pos + font_size < CLUSTER_BOX_X + CLUSTER_BOX_WIDTH - font_size:
                    cluster_box_lines[current_cluster_box_line] += event.unicode
                elif active_box == "types" and types_box_cursor_visible and cursor_pos + font_size < TYPES_BOX_X + TYPES_BOX_WIDTH - font_size:
                    types_box_lines[current_types_box_line] += event.unicode

    # Check if the cursor is inside each button
    mouse_pos = pygame.mouse.get_pos()

    # Button 1
    if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
        button1_color = BLUED
    else:
        button1_color = ORANGE

    # Draw the buttons
    pygame.draw.rect(screen, button1_color, pygame.Rect(button_x, button_y, button_width, button_height), 0, 18)
    pygame.draw.rect(screen, BLUED, pygame.Rect(button_x, button_y, button_width, button_height), 4, 18)

    # Draw button text
    txt_render = font_bold.render("Random It", True, WHITE)
    txt_button1 = txt_render.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
    screen.blit(txt_render, txt_button1)

    # Update display
    pygame.display.update()

    # Set maximum frame rate
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()
