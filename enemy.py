import heapq
import pygame
import math

class Enemy:
    def __init__(self, start_position, target_position, map_data, positions, tile_size):
        self.start_position = start_position
        self.target_position = target_position
        self.spawn = [start_position[0], start_position[1]]
        self.map_data = map_data
        self.positions = positions
        self.tile_size = tile_size
        self.speed = 0.07
        self.is_on_ladder = 0
        self.clock = pygame.time.Clock()
        self.target = target_position
        self.prekoracil = 0
        self.reached = False
        self.left = False

        # Initialize the path
        self.path = self.astar(target_position[0], target_position[1], False)
        self.a, self.b = self.path[1]
        self.x, self.y = self.path[0]

        self.catch_sound = pygame.mixer.Sound("fail.wav")

    def astar(self, playerX, playerY, hidden):
        self.reached = False
        start_node = math.floor(self.start_position[0]), math.floor(self.start_position[1])
        target_node = math.floor(self.target_position[0]), math.floor(self.target_position[1])

        player_rect = pygame.Rect(playerX * 32, playerY * 32, 24, 48)
        enemy_rect = pygame.Rect(self.start_position[0] * 32, self.start_position[1] * 32, 32, 32)

        if player_rect.colliderect(enemy_rect) and not hidden:
            self.reached = True
            self.catch_sound.play()
            self.start_position = self.spawn
            start_node = (self.start_position[0], self.start_position[1])

        if not self.is_valid_tile(target_node):
            target_node = (1, target_node)
            valid = self.neighbors(target_node)
            if len(valid) == 0:
                target_node = self.target
            else:
                target_node = valid[0]

        open_set = [(0, start_node)]
        came_from = {start_node: None}
        cost_so_far = {start_node: 0}

        while open_set:
            current = heapq.heappop(open_set)

            if current[1] == target_node:
                # Reconstruct the path
                current = current[1]
                path = []
                while current in came_from:
                    path.insert(0, current)
                    current = came_from[current]

                self.target = target_node
                return path

            for next_node in self.neighbors(current):
                new_cost = cost_so_far[current[1]] + 1  # Assuming equal cost for all tiles

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(next_node, target_node)
                    heapq.heappush(open_set, (priority, next_node))
                    came_from[next_node] = current[1]

        return []

    def neighbors(self, node):
        x, y = node[1]
        adjacent_tiles = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        # Filter out tiles outside the map and obstacles
        valid_neighbors = [tile for tile in adjacent_tiles if self.is_valid_tile(tile)]
        return valid_neighbors

    def is_valid_tile(self, tile):
        x, y = tile
        return 0 <= x < len(self.map_data[0]) and 0 <= y < len(self.map_data) and self.map_data[y][x] in ['G', 'L']

    def heuristic(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return abs(x1 - x2) + abs(y1 - y2)

    def render(self, screen, tileset, tile_rects, x, y):
        source_char = pygame.Rect(tile_rects[0])
        target_char = pygame.Rect(x * 32, y * 32, 32, 32)

        scaled_tile = pygame.transform.scale(tileset.subsurface(source_char), (32, 32))

        screen.blit(scaled_tile, target_char)


    def handle_controls(self):
        dt = self.clock.tick(60) / 20.0
        if dt > 1:
            dt = 0.9

        x1 = self.start_position[0]
        y1 = self.start_position[1]

        if len(self.path) > 1 or not self.prekoracil:

            if self.prekoracil or self.start_position == self.spawn:
                self.a, self.b = self.path[1]
                self.x, self.y = self.path[0]
                self.prekoracil = 0

            if self.a > self.x:     # desno
                self.start_position = (x1 + self.speed * dt, y1)

                if math.fabs(self.start_position[0] - self.a) <= self.speed:
                    self.prekoracil = 1
            elif self.a < self.x:   # levo
                self.start_position = (x1 - self.speed * dt, y1)
                self.left = True

                if math.fabs(self.start_position[0] - self.a) <= self.speed:
                    self.prekoracil = 1
                    a2 = self.start_position[0] + self.a-self.start_position[0]
                    self.start_position = (a2, self.start_position[1])
            elif self.b > self.y:   # dol
                self.start_position = (x1, y1 + self.speed * dt)

                if math.fabs(self.start_position[1] - self.b) <= self.speed:
                    self.prekoracil = 1
            elif self.b < self.y:   # gor
                self.start_position = (x1, y1 - self.speed * dt)

                if math.fabs(self.start_position[1] - self.b) <= self.speed:
                    self.prekoracil = 1
                    b2 = self.start_position[1] + self.b-self.start_position[1]
                    self.start_position = (self.start_position[0], b2)


class Enemy2:
    def __init__(self, left, right, y, direction):
        self.left = left
        self.right = right
        self.x = left
        self.y = y
        self.speed = 0.05
        self.direction = direction
        self.catch_sound = pygame.mixer.Sound("fail.wav")
        self.clock = pygame.time.Clock()

    def render(self, screen, tileset, tile_rects, x, y):
        source_char = pygame.Rect(tile_rects[1])
        target_char = pygame.Rect(x * 32, y * 32, 32, 32)

        scaled_tile = pygame.transform.scale(tileset.subsurface(source_char), (32, 32))

        screen.blit(scaled_tile, target_char)

    def handle_controls(self):
        dt = self.clock.tick(60) / 20.0
        if dt > 1:
            dt = 0.9
        if self.direction == "left":
            self.x -= self.speed * dt
            if self.x <= self.left:
                self.direction = "right"
        else:
            self.x += self.speed * dt
            if self.x >= self.right:
                self.direction = "left"

    def check_collision(self, playerX, playerY):
        player_rect = pygame.Rect(playerX * 32, playerY * 32, 24, 48)
        enemy_rect = pygame.Rect(self.x * 32, self.y * 32, 32, 32)

        if player_rect.colliderect(enemy_rect):
            self.catch_sound.play()
            return True
        return False
