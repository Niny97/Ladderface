from level import *
from files import *
from menu import *
import time
import random

BLACK = (10, 10, 10)
LAYERS1 = {"Map", "Top"}
win_image = pygame.image.load("win.png")
defeat_image = pygame.image.load("defeat.png")


class Game:
    def __init__(self, screen, objects, obj_rects, buttons, button_rects):
        pygame.init()
        pygame.display.set_caption("Ladderface")
        self.screen = screen

        self.levels = [Level(0), Level(1), Level(2)]
        self.lvl = 0
        self.is_running = True

        self.objects = objects
        self.obj_rects = obj_rects
        self.heartsN = 3

        self.font = pygame.font.Font(None, 36)
        self.collected_text = self.font.render("{:02d}/{}".format(self.levels[self.lvl].player.crystals,
                                                              self.levels[self.lvl].crystals), True, (0, 0, 0))
        self.text_rect = self.collected_text.get_rect(topright=(28.8*32, 5))

        menu_image = pygame.image.load("paused.png")
        resume_button = Button(screen, button_rects[10], 371, 252, "resume", buttons, "resume")
        restart_button = Button(screen, button_rects[11], 371, 352, "restart", buttons, "restart")
        to_menu_button = Button(screen, button_rects[9], 371, 452, "menu", buttons, "menu")
        self.menu = InGameMenu(self.screen, menu_image, [resume_button, restart_button, to_menu_button])
        self.buttons = buttons
        self.button_rects = button_rects
        self.win_sound = pygame.mixer.Sound("win.wav")
        self.defeat_sound = pygame.mixer.Sound("defeat.wav")
        self.next = ""

        self.last = time.time()
        self.time_since_last = 6

    def run(self):
        self.next = ""
        self.levels[self.lvl].start_time = time.time()
        self.is_running = True

        while self.is_running:
            if self.levels[self.lvl].player.collected:
                LAYERS1.add("Door")
            self.levels[self.lvl].player.handle_controls(self.levels[self.lvl].player.clock)
            self.levels[self.lvl].player.check_collisions(self.levels[self.lvl].map, self.levels[self.lvl].cset,
                                                          self.levels[self.lvl].crystals)
            for e in self.levels[self.lvl].enemies:
                if self.levels[self.lvl].player.hidden:
                    if self.time_since_last >= 6:
                        e.target_position = (random.choice(e.positions))
                        print("New target: {}".format(e.target_position))
                        self.last = time.time()
                else:
                    e.target_position = (self.levels[self.lvl].player.x, self.levels[self.lvl].player.y + 0.75)

                e.path = e.astar(self.levels[self.lvl].player.x, self.levels[self.lvl].player.y, self.levels[self.lvl].player.hidden)
                #print(e.path)
                if e.reached:
                    self.heartsN -= 1
                    self.levels[self.lvl].player.x, self.levels[self.lvl].player.y = \
                        self.levels[self.lvl].player.spawn[0], self.levels[self.lvl].player.spawn[1]

                e.handle_controls()

            for e2 in self.levels[self.lvl].enemies2:
                e2.handle_controls()
                if e2.check_collision(self.levels[self.lvl].player.x, self.levels[self.lvl].player.y):
                    self.heartsN -= 1
                    self.levels[self.lvl].player.x, self.levels[self.lvl].player.y = \
                        self.levels[self.lvl].player.spawn[0], self.levels[self.lvl].player.spawn[1]

            if self.heartsN == 0:
                self.defeat_sound.play()
                self.levels[self.lvl].player.score = (int) (len(self.levels[self.lvl].cset) * 100 - self.levels[self.lvl].time * 2)
                print(self.levels[self.lvl].time)
                end_menu = EndMenu(self.screen, defeat_image, [Button(self.screen, self.button_rects[8], 244, 459, "restart", self.buttons, "restart"),
                                                            Button(self.screen, self.button_rects[9], 498, 459, "menu", self.buttons, "menu")], self.lvl, player=self.levels[self.lvl].player)
                self.next = end_menu.run()
                self.is_running = False
                break
            self.time_since_last = time.time() - self.last
            self.collected_text = self.font.render("{:02d}/{}".format(len(self.levels[self.lvl].cset),
                                                                  self.levels[self.lvl].crystals), True, (0, 0, 0))
            self.render()
            self.handle_events()
            if self.levels[self.lvl].player.win:
                self.win_sound.play()
                self.levels[self.lvl].player.score = (int) (len(self.levels[self.lvl].cset) * 100 - self.levels[self.lvl].time * 2 + 50 * self.heartsN)
                end_menu = EndMenu(self.screen, win_image, [Button(self.screen, self.button_rects[8], 244, 459, "restart", self.buttons, "restart"),
                                                            Button(self.screen, self.button_rects[9], 498, 459, "menu", self.buttons, "menu")], self.lvl, player=self.levels[self.lvl].player)
                self.next = end_menu.run()
                self.is_running = False
        return self.next

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    t = time.time()
                    self.next = self.menu.run()
                    if self.next == "menu" or self.next == "restart":
                        self.is_running = False
                        break
                    t = time.time() - t
                    self.levels[self.lvl].start_time += t
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

    def render(self):
        self.screen.fill(BLACK)
        self.levels[self.lvl].render(self.screen, self.levels[self.lvl].map, LAYERS1, (32, 32))
        self.levels[self.lvl].player.render(self.screen, self.objects, self.obj_rects, self.levels[self.lvl].player.x,
                                            self.levels[self.lvl].player.y)
        render_map(self.screen, self.objects, self.obj_rects, self.levels[self.lvl].cmap, 32)
        self.levels[self.lvl].render(self.screen, self.levels[self.lvl].map, {"Bushes"}, (32, 32))
        for e in self.levels[self.lvl].enemies:
            e.render(self.screen, self.objects, self.obj_rects, e.start_position[0], e.start_position[1])

        for e2 in self.levels[self.lvl].enemies2:
            e2.render(self.screen, self.objects, self.obj_rects, e2.x, e2.y)

        self.draw_hearts()
        self.screen.blit(self.collected_text, self.text_rect)
        self.draw_time()
        pygame.display.flip()

    def draw_hearts(self):
        for i in range(0, self.heartsN):
            source_char = pygame.Rect(self.obj_rects[6])

            target_char = pygame.Rect(i * 32 + 5, 0, 32, 32)
            scaled_tile = pygame.transform.scale(self.objects.subsurface(source_char), (32, 32))
            self.screen.blit(scaled_tile, target_char)
        for i in range(self.heartsN, 3):
            source_char = pygame.Rect(self.obj_rects[7])
            target_char = pygame.Rect(i * 32 + 5, 0, 32, 32)
            scaled_tile = pygame.transform.scale(self.objects.subsurface(source_char), (32, 32))
            self.screen.blit(scaled_tile, target_char)

    def draw_time(self):
        self.levels[self.lvl].time = time.time() - self.levels[self.lvl].start_time
        hours, remainder = divmod(self.levels[self.lvl].time, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_text = self.font.render("{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds)), True, (0, 0, 0))
        self.screen.blit(time_text, time_text.get_rect(center=(15*32, 16)))

    def restart(self):
        self.heartsN = 3
        self.levels[self.lvl].restart()
        if "Door" in LAYERS1:
            LAYERS1.remove("Door")
