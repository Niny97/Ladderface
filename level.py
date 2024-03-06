import pytmx
import pygame
from player import *
from enemy import *
from files import *
import time


class Level:
    def __init__(self, level_number):
        self.cset = set()
        self.time = 0
        self.start_time = 0
        if level_number == 0:
            self.num = level_number
            self.map = pytmx.load_pygame("Map1.tmx")
            self.crystals = 22
            self.cmap_name = "Crystals1.csv"
            self.cmap_name_copy = "Crystals1_copy.csv"

            self.player = Player(7, 17.5, 0.0, 0.01, 0.01, "Crystals1_copy.csv")
            wmap, wpositions = convert_csv_to_map("Walkable.csv")
            self.enemies = [Enemy((13, 3), (11, 15), wmap, wpositions, (32, 32))]
            self.enemies2 = []
        elif level_number == 1:
            self.num = level_number
            self.map = pytmx.load_pygame("Map2.tmx")
            self.crystals = 22
            self.cmap_name = "Crystals2.csv"
            self.cmap_name_copy = "Crystals2_copy.csv"
            self.player = Player(15, 12.5, 0.0, 0.01, 0.01, "Crystals2_copy.csv")
            wmap, wpositions = convert_csv_to_map("Walkable2.csv")
            self.enemies = [Enemy((9, 4), (self.player.x, self.player.y), wmap, wpositions, (32, 32))]
            self.enemies2 = [Enemy2(19, 25, 5, "right")]
        elif level_number == 2:
            self.num = level_number
            self.map = pytmx.load_pygame("Map3.tmx")
            self.crystals = 22
            self.cmap_name = "Crystals3.csv"
            self.cmap_name_copy = "Crystals3_copy.csv"
            self.player = Player(15, 14.5, 0.0, 0.01, 0.01, "Crystals3_copy.csv")
            wmap, wpositions = convert_csv_to_map("Walkable3.csv")
            self.enemies = [Enemy((12, 2), (self.player.x, self.player.y), wmap, wpositions, (32, 32))]
            self.enemies2 = [Enemy2(23, 27, 12, "right"), Enemy2(3, 9, 9, "right")]
        self.cmap = copy_csv(self.cmap_name, self.cmap_name_copy)

    def render(self, screen, map, layers_to_draw, target_tile_size):
        for layer in map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in layers_to_draw:
                for x, y, gid in layer:
                    tile = map.get_tile_image_by_gid(gid)
                    if tile:
                        scaled_tile = pygame.transform.scale(tile, target_tile_size)
                        screen.blit(scaled_tile, (x * target_tile_size[0], y * target_tile_size[1]))


    def restart(self):
        self.cset = set()
        self.cmap = copy_csv(self.cmap_name, self.cmap_name_copy)
        self.player.x = self.player.spawn[0]
        self.player.y = self.player.spawn[1]
        self.time = 0
        self.start_time = 0
        self.player.crystals = 0
        self.player.direction = "down"
        self.player.win = False
        self.player.collected = False
        for enemy in self.enemies:
            enemy.start_position = enemy.spawn
