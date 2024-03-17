import pytmx
from files import *
from config import *


class Player:
    def __init__(self, x, y, crystal_map):
        self.x = x
        self.y = y
        self.spawn = [x, y]
        self.speed = 0.0
        self.acceleration = 0.01
        self.deceleration = 0.01
        self.x2 = 0
        self.y2 = 0

        self.is_on_ground = 0
        self.is_on_ladder = 0
        self.direction = "down"

        self.crystals = 0
        self.crystal_map = crystal_map
        self.coin_sound = pygame.mixer.Sound("coin.wav")
        self.hidden = False

        self.clock = pygame.time.Clock()
        self.win = False
        self.collected = False

    def handle_controls(self, clock):
        dt = clock.tick(60) / 20.0  # Get the time passed since the last call
        if dt > 1:
            dt = 0.9

        keys = pygame.key.get_pressed()

        if self.is_on_ground == 0 and self.is_on_ladder == 0:
            if self.speed < 0.1:
                self.speed += self.acceleration * dt
                if self.speed > 0.1:
                    self.speed = 0.1
            self.y += self.speed
            self.y2 = 1
            self.direction = "down"

        else:
            if keys[pygame.K_w]:
                self.direction = "up"
                if self.is_on_ladder:
                    if self.speed < 0.1:
                        self.speed += self.acceleration * dt
                    self.y -= self.speed * dt
                    self.y2 = -1
                    self.x2 = 0

            elif keys[pygame.K_s]:
                self.direction = "down"
                if self.is_on_ladder:
                    if self.speed < 0.1:
                        self.speed += self.acceleration * dt
                    self.y += self.speed * dt
                    self.y2 = 1
                    self.x2 = 0

            elif keys[pygame.K_a]:
                self.direction = "left"
                if self.speed < 0.1:
                    self.speed += self.acceleration * dt
                self.x -= self.speed * dt
                self.x2 = -1
                self.y2 = 0

            elif keys[pygame.K_d]:
                self.direction = "right"
                if self.speed < 0.1:
                    self.speed += self.acceleration * dt
                self.x += self.speed * dt
                self.x2 = 1
                self.y2 = 0

            else:
                if self.speed > 0:
                    self.speed -= self.deceleration * dt
                    self.x += self.x2 * self.speed * dt
                    self.y += self.y2 * self.speed * dt

        self.is_on_ladder = 0

    def render(self, screen, tileset, tile_rects, x, y):
        source_char = pygame.Rect(tile_rects[2])
        target_char = pygame.Rect(x * 32, y * 32, 17, 48)

        scaled_tile = pygame.transform.scale(tileset.subsurface(source_char), (24, 48))

        screen.blit(scaled_tile, target_char)

    def check_collisions(self, map, cset, cnum):
        scale_factor = (32 / 128)
        self.hidden = False

        for layer in map.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    player_rect = pygame.Rect(self.x * 32, self.y * 32, 24, 48)
                    obj_rect = pygame.Rect(obj.x * scale_factor, obj.y * scale_factor, obj.width * scale_factor,
                                           obj.height * scale_factor)

                    # Collisions
                    if player_rect.colliderect(obj_rect):
                        match layer.name:

                            case "Walls":
                                match self.direction:

                                    case "down":
                                        # print(player.x, player.y, obj_rect.x, obj_rect.y)
                                        self.y = obj_rect.y / 32 - 1.5
                                        self.is_on_ground = 1
                                    case "up":
                                        self.y = obj_rect.y / 32 + obj_rect.height / 32
                                    case "left":
                                        self.x = obj_rect.x / 32 + obj_rect.width / 32
                                    case "right":
                                        self.x = obj_rect.x / 32 - 0.75

                            case "Ladders":
                                self.is_on_ladder = 1
                                self.is_on_ground = 0
                                if self.y + 1.5 < obj_rect.y / 32:
                                    self.y = obj_rect.y / 32

                            case "Crystals":
                                if obj.id not in cset and config["settings"]["sfx"] == "on":
                                    self.coin_sound.play()

                                row = int(obj_rect.y / 32)
                                col = int(obj_rect.x / 32)
                                modify_csv(self.crystal_map, row, col, -1)
                                cset.add(obj.id)

                                if len(cset) == cnum:
                                    self.collected = True

                            case "Bushes":
                                self.hidden = True

                            case "Door":
                                if self.collected:
                                    self.win = True
