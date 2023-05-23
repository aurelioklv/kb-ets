import pygame
import sys
import time
import subprocess

pygame.init()

# Define screen size
SCREEN_WIDTH = 1123
SCREEN_HEIGHT = 790

# Define graph box size and position
GRAPH_BOX_WIDTH = 318
GRAPH_BOX_HEIGHT = 284
GRAPH_BOX_X = 92
GRAPH_BOX_Y = 402

# Define node box size and position
NODE_BOX_WIDTH = 318
NODE_BOX_HEIGHT = 284
NODE_BOX_X = 92
NODE_BOX_Y = 68

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Text Input")
clock = pygame.time.Clock()

# Define colors
BG = (224, 251, 252)
WHITE = (255, 255, 255)
BLUEL = (152, 193, 217)
BLUED = (61,90,128)
ORANGE = (238,108,77)
BLACK = (0,0,0)

# Define button properties
button_width = 148.36
button_height = 56.32
button_x = 177
button_y = 717

# Define button state
button1_clicked = False

# Define font
font_size = 18
font = pygame.font.Font('Poppins-Medium.ttf', font_size)
font_med = pygame.font.Font('Poppins-Medium.ttf', 26)
font_semi = pygame.font.Font('Poppins-SemiBold.ttf', 55)
font_bold= pygame.font.Font('Poppins-Bold.ttf', 20)

# Create empty list for lines of text
graph_box_lines = [""]
node_box_lines = [""]
current_graph_box_line = 0
current_node_box_line = 0

# For outputting text onto the screen
txt = "MAP REGION"
txt_ = "RANDOMIZER"
txt_title = font_semi.render(txt, True, WHITE)
txt_title_1 = font_semi.render(txt_, True, WHITE)
title_pos = txt_title.get_rect(center=(506 +520/2,28+184/4))
title_pos_1 = txt_title_1.get_rect(center=(506 +520/2,28+184*3/4))
txt_1 = "Types :"
txt_node = font_med.render(txt_1, True, WHITE)
txt_2 = "Graph Data :"
txt_graph = font_med.render(txt_2, True, WHITE)

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def save_text_to_file(lines, filename):
    text = "\n".join(lines) 
    with open(filename, 'w') as file:
        file.write(text)

def render_and_show_solution():
    if node_box_lines:
        save_text_to_file(node_box_lines, "types.txt")
        print("Teks telah disimpan dalam file", "types.txt")
    if graph_box_lines:
        save_text_to_file(graph_box_lines, "clusters.txt")
        print("Teks telah disimpan dalam file", "clusters.txt")
    subprocess.call(["python", "main.py"])
    # time.sleep(5)
    imp = pygame.image.load("D:\kb_ets\solution.png")
    screen.blit(imp, (456, 228))

# Game loop
run = True
graph_box_cursor_visible = True
node_box_cursor_visible = True
graph_box_cursor_timer = time.time()
node_box_cursor_timer = time.time()
active_box = "graph"  # Initially set active box to graph

# Update background
screen.fill(BG)
pygame.draw.rect(screen, BLUEL, pygame.Rect(506,28,520,184), 0, 19)
pygame.draw.rect(screen, BLUED, pygame.Rect(506,28,520,184), 5, 19)
screen.blit(txt_title, title_pos)
screen.blit(txt_title_1, title_pos_1)

while run:
    pygame.draw.rect(screen, BLUEL, pygame.Rect(71,15, 360, 688), 0, 41)
    pygame.draw.rect(screen, BLUED, pygame.Rect(71,15, 360, 688), 5, 41)

    pygame.draw.rect(screen, ORANGE, pygame.Rect(NODE_BOX_X,NODE_BOX_Y,NODE_BOX_WIDTH,NODE_BOX_HEIGHT), 5, 15)
    screen.blit(txt_node, (95, 30))

    pygame.draw.rect(screen, ORANGE, pygame.Rect(GRAPH_BOX_X,GRAPH_BOX_Y,GRAPH_BOX_WIDTH,GRAPH_BOX_HEIGHT), 5, 15)
    screen.blit(txt_graph, (95,363))

    # Display typed input in the graph box
    for i, line in enumerate(graph_box_lines):
        draw_text(line, font, WHITE, GRAPH_BOX_X + 15, GRAPH_BOX_Y + 5 + (i * font_size))

    # Display typed input in the node box
    for i, line in enumerate(node_box_lines):
        draw_text(line, font, WHITE, NODE_BOX_X + 15, NODE_BOX_Y + 5 + (i * font_size))

    # Draw blinking cursor in the graph box
    if active_box == "graph":
        if time.time() - graph_box_cursor_timer >= 0.5:
            graph_box_cursor_visible = not graph_box_cursor_visible
            graph_box_cursor_timer = time.time()

        if graph_box_cursor_visible:
            cursor_pos = font.size(graph_box_lines[current_graph_box_line])[0] + GRAPH_BOX_X + 15
            cursor_y = GRAPH_BOX_Y + 5 + (current_graph_box_line * font_size)
            pygame.draw.line(screen, ORANGE, (cursor_pos, cursor_y), (cursor_pos, cursor_y + font_size), 2)

    # Draw blinking cursor in the node box
    if active_box == "node":
        if time.time() - node_box_cursor_timer >= 0.5:
            node_box_cursor_visible = not node_box_cursor_visible
            node_box_cursor_timer = time.time()

        if node_box_cursor_visible:
            cursor_pos = font.size(node_box_lines[current_node_box_line])[0] + NODE_BOX_X + 15
            cursor_y = NODE_BOX_Y + 5 + (current_node_box_line * font_size)
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

            # Check if the graph box is clicked
            if GRAPH_BOX_X <= mouse_pos[0] <= GRAPH_BOX_X + GRAPH_BOX_WIDTH and GRAPH_BOX_Y <= mouse_pos[1] <= GRAPH_BOX_Y + GRAPH_BOX_HEIGHT:
                active_box = "graph"
            # Check if the node box is clicked
            elif NODE_BOX_X <= mouse_pos[0] <= NODE_BOX_X + NODE_BOX_WIDTH and NODE_BOX_Y <= mouse_pos[1] <= NODE_BOX_Y + NODE_BOX_HEIGHT:
                active_box = "node"

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if active_box == "graph":
                    if current_graph_box_line >= 0 and len(graph_box_lines[current_graph_box_line]) > 0:
                        graph_box_lines[current_graph_box_line] = graph_box_lines[current_graph_box_line][:-1]
                    elif current_graph_box_line > 0 and len(graph_box_lines[current_graph_box_line]) == 0:
                        graph_box_lines.pop(current_graph_box_line)
                        current_graph_box_line -= 1
                elif active_box == "node":
                    if current_node_box_line >= 0 and len(node_box_lines[current_node_box_line]) > 0:
                        node_box_lines[current_node_box_line] = node_box_lines[current_node_box_line][:-1]
                    elif current_node_box_line > 0 and len(node_box_lines[current_node_box_line]) == 0:
                        node_box_lines.pop(current_node_box_line)
                        current_node_box_line -= 1

            elif event.key == pygame.K_RETURN:
                if active_box == "graph" and graph_box_cursor_visible and cursor_y + font_size < GRAPH_BOX_Y + GRAPH_BOX_HEIGHT - font_size:
                    graph_box_lines.insert(current_graph_box_line + 1, "")
                    current_graph_box_line += 1
                elif active_box == "node" and node_box_cursor_visible and cursor_y + font_size < NODE_BOX_Y + NODE_BOX_HEIGHT - font_size:
                    node_box_lines.insert(current_node_box_line + 1, "")
                    current_node_box_line += 1

            elif event.key == pygame.K_UP:
                if active_box == "graph" and current_graph_box_line > 0 and graph_box_cursor_visible:
                    current_graph_box_line -= 1
                elif active_box == "node" and current_node_box_line > 0 and node_box_cursor_visible:
                    current_node_box_line -= 1

            elif event.key == pygame.K_DOWN:
                if active_box == "graph" and current_graph_box_line < len(graph_box_lines) - 1 and graph_box_cursor_visible:
                    current_graph_box_line += 1
                elif active_box == "node" and current_node_box_line < len(node_box_lines) - 1 and node_box_cursor_visible:
                    current_node_box_line += 1

            else:
                if active_box == "graph" and graph_box_cursor_visible and cursor_pos + font_size < GRAPH_BOX_X + GRAPH_BOX_WIDTH - font_size:
                    graph_box_lines[current_graph_box_line] += event.unicode
                elif active_box == "node" and node_box_cursor_visible and cursor_pos + font_size < NODE_BOX_X + NODE_BOX_WIDTH - font_size:
                    node_box_lines[current_node_box_line] += event.unicode

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
    txt_render = font_bold.render("Render It", True, WHITE)
    txt_button1 = txt_render.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
    screen.blit(txt_render, txt_button1)

    # Update display
    pygame.display.update()

    # Set maximum frame rate
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()
