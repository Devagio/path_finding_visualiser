import pygame
from queue import PriorityQueue


def reconstruct_path(came_from, current, do_draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        do_draw()


def dijkstra(do_draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, do_draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            if g_score[current] + 1 < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = g_score[current] + 1
                if neighbour not in open_set_hash:
                    count = count + 1
                    open_set.put((g_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        do_draw()

        if current != start:
            current.make_closed()

    return False
