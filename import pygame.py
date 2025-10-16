import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 1000, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer — Bubble, Insertion, Selection, Quick, Merge")


BLACK = (10, 15, 25)
WHITE = (235, 235, 235)
RED = (239, 68, 68)
GREEN = (16, 185, 129)
BLUE = (59, 130, 246)
YELLOW = (234, 179, 8)
PURPLE = (147, 51, 234)
CYAN = (6, 182, 212)
GRAY = (130, 130, 130)


NUM_BARS = 80
BAR_WIDTH = WIDTH // NUM_BARS
FPS = 60

font = pygame.font.SysFont("consolas", 20)


def draw_bars(values, colors):
    WIN.fill(BLACK)
    for i, val in enumerate(values):
        x = i * BAR_WIDTH
        y = HEIGHT - val
        pygame.draw.rect(WIN, colors[i], (x, y, BAR_WIDTH - 2, val))
    pygame.display.update()

def generate_array(n):
    return [random.randint(20, HEIGHT - 60) for _ in range(n)]

def show_text(text):
    label = font.render(text, True, WHITE)
    WIN.blit(label, (20, 20))
    pygame.display.update()



def bubble_sort(values):
    n = len(values)
    for i in range(n):
        for j in range(0, n - i - 1):
            colors = [WHITE] * n
            colors[j], colors[j+1] = RED, BLUE
            draw_bars(values, colors)
            yield True
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
    for i in range(n):
        draw_bars(values, [GREEN]*n)
        yield True

def insertion_sort(values):
    for i in range(1, len(values)):
        key = values[i]
        j = i - 1
        while j >= 0 and values[j] > key:
            values[j + 1] = values[j]
            j -= 1
            colors = [WHITE]*len(values)
            colors[i] = BLUE
            colors[j] = RED if j >= 0 else RED
            draw_bars(values, colors)
            yield True
        values[j + 1] = key
    for i in range(len(values)):
        draw_bars(values, [GREEN]*len(values))
        yield True

def selection_sort(values):
    n = len(values)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            colors = [WHITE]*n
            colors[min_idx] = BLUE
            colors[j] = RED
            draw_bars(values, colors)
            yield True
            if values[j] < values[min_idx]:
                min_idx = j
        values[i], values[min_idx] = values[min_idx], values[i]
    for i in range(n):
        draw_bars(values, [GREEN]*n)
        yield True

def quick_sort(values, low, high):
    if low < high:
        pivot = values[high]
        i = low - 1
        for j in range(low, high):
            colors = [WHITE]*len(values)
            colors[j], colors[high] = RED, BLUE
            draw_bars(values, colors)
            yield True
            if values[j] <= pivot:
                i += 1
                values[i], values[j] = values[j], values[i]
        values[i+1], values[high] = values[high], values[i+1]
        yield from quick_sort(values, low, i)
        yield from quick_sort(values, i+2, high)
    yield True

def merge_sort(values, left, right):
    if left >= right:
        return
    mid = (left + right) // 2
    yield from merge_sort(values, left, mid)
    yield from merge_sort(values, mid + 1, right)
    merge(values, left, mid, right)
    yield True

def merge(values, left, mid, right):
    left_part = values[left:mid + 1]
    right_part = values[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        colors = [WHITE]*len(values)
        colors[k] = CYAN
        draw_bars(values, colors)
        yield True
        if left_part[i] <= right_part[j]:
            values[k] = left_part[i]
            i += 1
        else:
            values[k] = right_part[j]
            j += 1
        k += 1
    while i < len(left_part):
        values[k] = left_part[i]
        i += 1
        k += 1
        yield True
    while j < len(right_part):
        values[k] = right_part[j]
        j += 1
        k += 1
        yield True


def main():
    clock = pygame.time.Clock()
    values = generate_array(NUM_BARS)
    sorting = False
    algo_generator = None
    sorting_name = ""

    running = True
    while running:
        clock.tick(FPS)
        WIN.fill(BLACK)
        draw_bars(values, [PURPLE]*len(values))
        show_text("1:Bubble  2:Insertion  3:Selection  4:Quick  5:Merge  R:Reset  ESC:Quit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    values = generate_array(NUM_BARS)
                    sorting = False
                    algo_generator = None
                elif not sorting:
                    if event.key == pygame.K_1:
                        sorting = True
                        sorting_name = "Bubble Sort"
                        algo_generator = bubble_sort(values)
                    elif event.key == pygame.K_2:
                        sorting = True
                        sorting_name = "Insertion Sort"
                        algo_generator = insertion_sort(values)
                    elif event.key == pygame.K_3:
                        sorting = True
                        sorting_name = "Selection Sort"
                        algo_generator = selection_sort(values)
                    elif event.key == pygame.K_4:
                        sorting = True
                        sorting_name = "Quick Sort"
                        algo_generator = quick_sort(values, 0, len(values)-1)
                    elif event.key == pygame.K_5:
                        sorting = True
                        sorting_name = "Merge Sort"
                        algo_generator = merge_sort(values, 0, len(values)-1)

        if sorting:
            try:
                next(algo_generator)
                show_text(f"{sorting_name} in progress...")
            except StopIteration:
                sorting = False
                draw_bars(values, [GREEN]*len(values))
                show_text(f"{sorting_name} completed!")

        pygame.display.flip()

if __name__ == "__main__":
    main()
