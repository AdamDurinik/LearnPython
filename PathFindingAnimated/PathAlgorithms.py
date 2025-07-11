from collections import deque
import heapq
import math

def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    queue.append(start)
    came_from = {start: None}
    visited = []

    while queue:
        current = queue.popleft()
        visited.append(current)

        if current == end:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows:
                if grid[ny][nx] == 0 and neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current

    return visited, reconstruct_path(came_from, start, end)


def dfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    stack = [start]
    came_from = {start: None}
    visited = []

    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.append(current)

        if current == end:
            break

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows:
                if grid[ny][nx] == 0 and neighbor not in came_from:
                    stack.append(neighbor)
                    came_from[neighbor] = current

    return visited, reconstruct_path(came_from, start, end)


def dijkstra(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    visited = []
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]

    while pq:
        cost, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.append(current)

        if current == end:
            break

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 1:
                new_cost = dist[current] + 1
                if neighbor not in dist or new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = current
                    heapq.heappush(pq, (new_cost, neighbor))

    return visited, reconstruct_path(prev, start, end)


def astar(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    open_set = [(heuristic(start, end), 0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    visited = []

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.append(current)

        if current == end:
            break

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 1:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    came_from[neighbor] = current

    return visited, reconstruct_path(came_from, start, end)


def greedy(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    open_set = [(heuristic(start, end), start)]
    came_from = {start: None}
    visited = []

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.append(current)

        if current == end:
            break

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] != 1:
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (heuristic(neighbor, end), neighbor))

    return visited, reconstruct_path(came_from, start, end)


def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, start, end):
    path = []
    cur = end
    while cur in came_from and came_from[cur] is not None:
        path.append(cur)
        cur = came_from[cur]
    if cur == start:
        path.reverse()
        return path
    return []
