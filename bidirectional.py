import pygame
from queue import PriorityQueue


def reconstruct_path(came_from, current, do_draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        do_draw()


def bidirectional(do_draw, grid, start, end):
    count_1 = 0
    count_2 = 0
    open_set_1 = PriorityQueue()
    open_set_2 = PriorityQueue()
    open_set_1.put((0, count_1, start))
    open_set_2.put((0, count_2, end))
    came_from_1 = {}
    came_from_2 = {}

    g_score_1 = {spot: float("inf") for row in grid for spot in row}
    g_score_1[start] = 0
    g_score_2 = {spot: float("inf") for row in grid for spot in row}
    g_score_2[end] = 0

    open_set_hash_1 = {start}
    open_set_hash_2 = {end}

    while not open_set_1.empty() and not open_set_2.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_1 = open_set_1.get()[2]
        open_set_hash_1.remove(current_1)

        if current_1 in open_set_hash_2:
            current_1.make_path()
            reconstruct_path(came_from_1, current_1, do_draw)
            reconstruct_path(came_from_2, current_1, do_draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current_1.neighbours:
            if g_score_1[current_1] + 1 < g_score_1[neighbour]:
                came_from_1[neighbour] = current_1
                g_score_1[neighbour] = g_score_1[current_1] + 1
                if neighbour not in open_set_hash_1:
                    count_1 = count_1 + 1
                    open_set_1.put((g_score_1[neighbour], count_1, neighbour))
                    open_set_hash_1.add(neighbour)
                    neighbour.make_open()

        do_draw()

        if current_1 != start:
            current_1.make_closed()

        current_2 = open_set_2.get()[2]
        open_set_hash_2.remove(current_2)

        if current_2 in open_set_hash_1:
            current_2.make_path()
            reconstruct_path(came_from_1, current_2, do_draw)
            reconstruct_path(came_from_2, current_2, do_draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current_2.neighbours:
            if g_score_2[current_2] + 1 < g_score_2[neighbour]:
                came_from_2[neighbour] = current_2
                g_score_2[neighbour] = g_score_2[current_2] + 1
                if neighbour not in open_set_hash_2:
                    count_2 = count_2 + 1
                    open_set_2.put((g_score_2[neighbour], count_2, neighbour))
                    open_set_hash_2.add(neighbour)
                    neighbour.make_open()

        do_draw()

        if current_2 != end:
            current_2.make_closed()

    return False
