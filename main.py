import pygame as pygame
from a_star import a_star
from dijkstra import dijkstra
from bidirectional import bidirectional


WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm Visualisation")
pygame.font.init()

RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 100, 0)
GREY = (170, 170, 170)

dictionary = {
    RED: "Already explored cell",
    GREEN: "Cell being currently explored",
    BLUE: "End Node",
    ORANGE: "Start Node",
    PURPLE: "Shortest Path",
    BLACK: "Barrier cell",
    WHITE: "Unexplored cell",
}

mouse_text = [
    ("The first left click will pick the start node", ORANGE),
    ("The second left click will pick the end node", BLUE),
    ("Further left clicks will place barriers", BLACK),
    ("Remove cell assignment with right click", WHITE)
]


class Spot:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.colour = WHITE
        self.neighbours = []
        self.size = size
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_barrier(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == BLUE

    def reset(self):
        self.colour = WHITE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = BLUE

    def make_path(self):
        self.colour = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.size, self.size))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbours.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbours.append(grid[self.row-1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbours.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbours.append(grid[self.row][self.col-1])


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)

    pygame.display.update()


def render_help(win):
    win.fill(GREY)

    title_font = pygame.font.Font("freesansbold.ttf", 32)
    title = title_font.render("Welcome to Path Finding Visualiser", True, BLACK)
    win.blit(title, (15, 15))
    pygame.draw.line(win, YELLOW, (15, 60), (WIDTH-15, 60))

    subtitle_font = pygame.font.Font("freesansbold.ttf", 16)
    subtitle = subtitle_font.render("Colour Codes:", True, BLACK)
    win.blit(subtitle, (40, 80))

    key_size = 16
    key_space = 24
    key_start_x = 200
    key_start_y = 80
    font_x = key_start_x + key_space
    for colour_name in [ORANGE, BLUE, BLACK, GREEN, RED, PURPLE, WHITE]:
        pygame.draw.rect(win, colour_name, (key_start_x, key_start_y, key_size, key_size))
        description = subtitle_font.render(dictionary[colour_name], True, BLACK)
        win.blit(description, (font_x, key_start_y))
        key_start_y = key_start_y + key_space
    pygame.draw.line(win, YELLOW, (15, 270), (WIDTH - 15, 270))

    subtitle_font = pygame.font.Font("freesansbold.ttf", 16)
    subtitle = subtitle_font.render("Mouse Use:", True, BLACK)
    win.blit(subtitle, (40, 300))

    key_start_y = 300
    font_x = 150
    for text, colour_name in mouse_text:
        description = subtitle_font.render(text, True, colour_name)
        win.blit(description, (font_x, key_start_y))
        key_start_y = key_start_y + key_space
    pygame.draw.line(win, YELLOW, (15, 415), (WIDTH - 15, 415))

    key_strokes = subtitle_font.render("Key Stroke Options:", True, BLACK)
    win.blit(key_strokes, (200, 440))

    key_use = "A -> A-star algorithm          B -> Bidirectional Dijkstra          D -> Dijkstras"
    additional = "C -> Clear Screen          H -> Toggle Help Screen"

    key_use_init = subtitle_font.render(key_use, True, BLACK)
    additional_init = subtitle_font.render(additional, True, BLACK)
    win.blit(key_use_init, (25, 490))
    win.blit(additional_init, (100, 520))

    description = subtitle_font.render("PRESS H TO BEGIN!", True, YELLOW)
    win.blit(description, (200, 560))

    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    rows = 50
    grid = make_grid(rows, width)

    start = None
    end = None

    run = True
    flag = False
    done = False

    while run:

        if flag:
            draw(win, grid, rows, width)
        else:
            render_help(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if flag and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif flag and pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    flag = not flag
                    if flag:
                        draw(win, grid, rows, width)
                    else:
                        render_help(win)

                if event.key == pygame.K_a and end and start and flag and not done:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    path_exist = a_star(lambda: draw(win, grid, rows, width), grid, start, end)
                    done = True

                    if not path_exist:
                        pass

                if event.key == pygame.K_b and end and start and flag and not done:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    path_exist = bidirectional(lambda: draw(win, grid, rows, width), grid, start, end)
                    done = True

                    if not path_exist:
                        pass

                if event.key == pygame.K_d and end and start and flag and not done:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    path_exist = dijkstra(lambda: draw(win, grid, rows, width), grid, start, end)
                    done = True

                    if not path_exist:
                        pass

                if event.key == pygame.K_c and flag:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
                    done = False

    pygame.quit()


main(WIN, WIDTH)
