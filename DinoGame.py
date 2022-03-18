import sys
import math
import random
import time
import matplotlib.pyplot as plt
import pandas as pd
import pygame
from pygame.locals import *


curr_fps = 0
screen_height = 720
screen_width = round(screen_height*(16/9))
gravity = 20
speed_x = 0
jump_speed = 2
score_speed = 0
score_multiplier = 5
ratio = math.ceil(screen_height/135)
pause = False
ai_mechanics = True

# AI
POP_SIZE = 200
GENE = 19
TOP_POP = 20
NUM_PARENT = math.floor(POP_SIZE/4)
MUTATE_RATE = 0.1
chromosome = [[0] * GENE] * POP_SIZE


class Dino(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.dino_sprite = pygame.image.load('dino.png').convert_alpha()
        crop_sprite = self.dino_sprite.subsurface(0, 0, 16,16)
        self.image = pygame.transform.scale(crop_sprite, (16*ratio, 16*ratio))

        self.rect = self.image.get_rect()
        self.rect.topleft = (10*ratio, round(screen_height/3)*2-16*ratio - 300)

        self.walk = 0
        self.jump = False
        self.crawl = False
        self.on_ground = False
        self.y_speed = 0
        self.walk_pose = 1 # adjust walk pose to 0 when for start button trigger exist

    def forward(self):
        self.walk += 1
        # print(self.walk)
        if self.walk > round(curr_fps / 5):
            if self.walk_pose == 1 and not self.crawl:
                crop_sprite = self.dino_sprite.subsurface(16, 0, 16, 16)
                self.walk_pose = 2
            elif self.walk_pose == 1 and self.crawl:
                crop_sprite = self.dino_sprite.subsurface(48, 0, 32, 8)
                self.walk_pose = 2
            elif self.walk_pose == 2 and not self.crawl:
                crop_sprite = self.dino_sprite.subsurface(32, 0, 16, 16)
                self.walk_pose = 1
            elif self.walk_pose == 2 and self.crawl:
                crop_sprite = self.dino_sprite.subsurface(48, 8, 32, 8)
                self.walk_pose = 1

            if not self.crawl:
                self.image = pygame.transform.scale(crop_sprite, (16 * ratio, 16 * ratio))
                self.rect.width = 16 * ratio
                self.rect.height = 16 * ratio
            else:
                self.image = pygame.transform.scale(crop_sprite, (32 * ratio, 8 * ratio))
                self.rect.width = 32 * ratio
                self.rect.height = 8 * ratio

            self.walk = 0

    def jumping(self):
        if self.jump and self.y_speed <= 0:
            self.y_speed = 48

        if self.y_speed > 0:
            self.jump = False
            self.rect.move_ip(0, -self.y_speed)
            self.y_speed -= jump_speed

    def jumps(self):
        if self.on_ground:
            self.jump = True
            self.on_ground = False

    def crawls(self):
        if self.on_ground and not self.crawl:
            self.rect.move_ip(0, 16 * ratio / 2)
            if self.walk_pose == 1:
                crop_sprite = self.dino_sprite.subsurface(48, 0, 32, 8)
                self.walk_pose = 2
            elif self.walk_pose == 2:
                crop_sprite = self.dino_sprite.subsurface(48, 8, 32, 8)
                self.walk_pose = 1
            self.image = pygame.transform.scale(crop_sprite, (32 * ratio, 8 * ratio))
            self.walk = 0
        if self.on_ground:
            self.crawl = True

    def uncrawl(self):
        if self.crawl:
            self.rect.move_ip(0, -16 * ratio / 2)
            if self.walk_pose == 1:
                crop_sprite = self.dino_sprite.subsurface(16, 0, 16, 16)
                self.walk_pose = 2
            elif self.walk_pose == 2:
                crop_sprite = self.dino_sprite.subsurface(32, 0, 16, 16)
                self.walk_pose = 1
            self.image = pygame.transform.scale(crop_sprite, (16 * ratio, 16 * ratio))
        self.crawl = False


class Obstacle(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Fetch the rectangle object that has the dimensions of the image
        self.x = -16*ratio - 1
        self.y = 0
        self.animate = 0
        self.animate_delay = 0
        self.random_obs = 0
        self.ratio = round(ratio * 0.6)
        self.collision = False

        self.obs = pygame.image.load('obstacles.png').convert_alpha()
        self.image = pygame.transform.scale(self.obs, (0, 0))

        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.x, self.y, 16*self.ratio, 16*self.ratio)
        self.rect.topleft = (self.x, self.y)

    def incoming(self, fps):
        if self.random_obs != 1:
            self.hitbox = pygame.Rect(self.x, self.y, 16 * self.ratio, 16 * self.ratio)
        else:
            self.hitbox = pygame.Rect(self.x, self.y, 16 * self.ratio, 32 * self.ratio)
        self.x -= round(speed_x * score_multiplier)
        self.rect.topleft = (self.x, self.y)

        if self.x < -16*self.ratio:
            self.random_obs = random.randint(0, 4)
            self.x = screen_width
            self.animate = 0
            self.animate_delay = 0

            if self.random_obs == 0:
                self.y = round(screen_height / 3) * 2 - 16 * self.ratio
                crop_obs = self.obs.subsurface(0, 0, 16, 16)
                self.image = pygame.transform.scale(crop_obs, (16*self.ratio, 16*self.ratio))
            elif self.random_obs == 1:
                self.y = round(screen_height / 3) * 2 - 32 * self.ratio
                crop_obs = self.obs.subsurface(16, 0, 16, 32)
                self.image = pygame.transform.scale(crop_obs, (16 * self.ratio, 32 * self.ratio))
            elif self.random_obs >= 2:
                if self.random_obs == 2:
                    self.y = round(screen_height / 3) * 2 - 16 * self.ratio
                elif self.random_obs == 3:
                    self.y = round(screen_height / 3) * 2 - 32 * self.ratio
                elif self.random_obs == 4:
                    self.y = round(screen_height / 3) * 2 - 48 * self.ratio
                crop_obs = self.obs.subsurface(32, 0, 16, 16)
                self.image = pygame.transform.scale(crop_obs, (16 * self.ratio, 16 * self.ratio))

        if self.random_obs >= 2:
            self.animate_delay += 1
            if self.animate_delay > fps/5:
                if self.animate == 0:
                    crop_obs = self.obs.subsurface(32, 0, 16, 16)
                    self.image = pygame.transform.scale(crop_obs, (16 * self.ratio, 16 * self.ratio))
                    self.animate = 1
                else:
                    crop_obs = self.obs.subsurface(32, 16, 16, 16)
                    self.image = pygame.transform.scale(crop_obs, (16 * self.ratio, 16 * self.ratio))
                    self.animate = 0
                self.animate_delay = 0

    def reset(self):
        self.x = -16 * ratio - 1
        self.y = 0
        self.animate = 0
        self.animate_delay = 0
        self.random_obs = 0
        self.ratio = round(ratio * 0.6)
        self.collision = False


class Grass(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, x_pos):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.x = x_pos
        self.y = round(screen_height/3)*2
        self.grass = pygame.image.load('grass.png').convert_alpha()
        # random img
        random_img = random.randint(0, 14)*16
        crop_grass = self.grass.subsurface(random_img, 0, 16, 45)
        self.image = pygame.transform.scale(crop_grass, (16*ratio, 45*ratio))
        self.rect = self.image.get_rect()

        # Basic Formula: x = 0*ratio, y = round(screen_height/3)*2
        self.rect.topleft = (self.x, self.y)

    def forward(self, curr_w_terrain):
        self.x -= round(speed_x * score_multiplier)
        self.rect.topleft = (self.x, round(screen_height/3)*2)

        if self.x < -curr_w_terrain:
            random_img = random.randint(0, 14) * 16
            crop_grass = self.grass.subsurface(random_img, 0, 16, 45)
            self.image = pygame.transform.scale(crop_grass, (16 * ratio, 45 * ratio))
            self.x += (curr_w_terrain * 17)


class Setting:
    def __init__(self):
        global speed_x, gravity, jump_speed
        #image
        self.menu = pygame.Surface((400, 230))
        self.menu = self.menu.convert_alpha()
        self.menu.set_alpha(192)
        self.menu.fill((105, 105, 105))
        self.menu_pos = ((screen_width/2)-(400/2), (screen_height/2)-(230/2))

        self.setting_string = "Setting"
        self.fps_string = "FPS                          " + str(60)
        self.ai_string = "AI                           "+str(ai_mechanics)
        self.font = pygame.font.SysFont('comicsansms', 24)
        self.name_display = self.font.render(self.setting_string, True, (0, 0, 0))
        self.fps_display = self.font.render(self.fps_string, True, (0, 0, 0))
        self.ai = self.font.render(self.ai_string, True, (0, 0, 0))

        self.center_width = (screen_width/2-self.fps_display.get_rect()[2]/2)
        self.center_height = (screen_height/2-self.fps_display.get_rect()[3]/2)
        self.fps_box = self.fps_display.get_rect().move(self.center_width, self.center_height-10)
        self.ai_box = self.ai.get_rect().move(self.center_width, self.center_height+30)

        self.raw_img = pygame.image.load("setting.png").convert_alpha()
        self.img = self.raw_img.subsurface(0, 0, 64, 64)
        self.img = pygame.transform.scale(self.img, (64, 64))
        self.pos_x = screen_width-74
        self.pos_y = 10
        self.rect = self.img.get_rect()
        self.rect.move_ip(self.pos_x, self.pos_y)
        self.collide = False
        self.setting_visible = False
        self.maintain = False
        self.collide_text = False
        self.setting_changed = False

        # 0=poor(30) 1=normal(60) 2=high(120)
        self.fps = 60
        self.score_modifier = 60/self.fps
        speed_x = 120.0 * 1 / self.fps
        # jump_speed = 120.0 / self.fps
        # gravity = round(jump_speed * 10)

    def optimize_perf(self):
        global speed, gravity, jump_speed
        self.score_modifier = 60/self.fps
        speed_x = 120.0 * (score_speed**(1)) / self.fps
        # jump_speed = 120.0 / 60
        # gravity = round(jump_speed * 10)

    def hover_setting(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.img = self.raw_img.subsurface(64, 0, 64, 64)
            self.img = pygame.transform.scale(self.img, (64, 64))
            self.collide = True
        else:
            self.img = self.raw_img.subsurface(0, 0, 64, 64)
            self.img = pygame.transform.scale(self.img, (64, 64))
            self.collide = False

    def hover_text(self, mouse_pos):
        if self.setting_visible:
            if self.fps_box.collidepoint(mouse_pos):
                self.fps_display = self.font.render(self.fps_string, True, (255, 255, 255))
                self.collide_text = True
            else:
                self.fps_display = self.font.render(self.fps_string, True, (0, 0, 0))
                self.collide_text = False

            if self.ai_box.collidepoint(mouse_pos):
                self.ai = self.font.render(self.ai_string, True, (255, 255, 255))
                self.collide_text = True
            else:
                self.ai = self.font.render(self.ai_string, True, (0, 0, 0))
                self.collide_text = False

    def click(self, mouse_pos):
        global pause, ai_mechanics
        if self.collide and not self.setting_visible and not self.maintain:
            self.setting_visible = True
            self.maintain = True
            pause = True
        elif self.collide and not self.setting_visible and self.maintain:
            pass
        elif self.collide and self.setting_visible and self.maintain:
            pass
        elif self.collide and self.setting_visible and not self.maintain:
            self.setting_visible = False
            self.maintain = True
            pause = False

        if self.fps_box.collidepoint(mouse_pos) and not self.setting_changed and not self.maintain:
            self.setting_changed = True
            self.maintain = True
            if self.fps == 30:
                self.fps = 60
            elif self.fps == 60:
                self.fps = 120
            elif self.fps == 120:
                self.fps = 30
            self.fps_string = "FPS                          " + str(self.fps)
        elif self.fps_box.collidepoint(mouse_pos) and not self.setting_changed and self.maintain:
            pass
        elif self.fps_box.collidepoint(mouse_pos) and self.setting_changed and self.maintain:
            pass
        elif self.fps_box.collidepoint(mouse_pos) and self.setting_changed and not self.maintain:
            self.setting_changed = False
            self.maintain = True
            if self.fps == 30:
                self.fps = 60
            elif self.fps == 60:
                self.fps = 120
            elif self.fps == 120:
                self.fps = 30
            self.fps_string = "FPS                          " + str(self.fps)

        if self.ai_box.collidepoint(mouse_pos) and not self.setting_changed and not self.maintain:
            self.setting_changed = True
            self.maintain = True
            if ai_mechanics:
                ai_mechanics = False
            elif not ai_mechanics:
                ai_mechanics = True
            self.ai_string = "AI                           " + str(ai_mechanics)
        elif self.ai_box.collidepoint(mouse_pos) and not self.setting_changed and self.maintain:
            pass
        elif self.ai_box.collidepoint(mouse_pos) and self.setting_changed and self.maintain:
            pass
        elif self.ai_box.collidepoint(mouse_pos) and self.setting_changed and not self.maintain:
            self.setting_changed = False
            self.maintain = True
            if ai_mechanics:
                ai_mechanics = False
                self.ai_string = "AI                           False"
            elif not ai_mechanics:
                ai_mechanics = True
                self.ai_string = "AI                           True"


def width_terrain():
    return round(screen_width/15)


def fall(dino, grasses):
    if dino.rect.y + (1.1 * 16 * ratio) < grasses[0].y and not dino.crawl:
        dino.rect.move_ip(0, gravity)
    elif dino.rect.y + (16 * ratio) < grasses[0].y and not dino.crawl:
        dino.rect.move_ip(0, round(gravity/4))
    elif dino.rect.y + (1.1 * 16 * ratio/2) < grasses[0].y and dino.crawl:
        dino.rect.move_ip(0, gravity)
    elif dino.rect.y + (16 * ratio/2) < grasses[0].y and dino.crawl:
        dino.rect.move_ip(0, round(gravity/4))
    else:
        dino.on_ground = True

    if dino.rect.y + (16 * ratio) > grasses[0].y and not dino.crawl:
        dino.rect.move_ip(0, -1)
    elif dino.rect.y + (16 * ratio / 2) > grasses[0].y and dino.crawl:
        dino.rect.move_ip(0, -1)


class AIntelligence:
    def __init__(self):
        self.plot_x = [] # Gen
        self.plot_y1 = [] # Score
        self.plot_y2 = []  # Score
        self.top_score = 0
        self.total_score = 0
        self.avg_score = 0

        self.fitness = [0]*POP_SIZE
        self.fitness_sum = 0

        self.select_parent = [[0]*GENE] * (NUM_PARENT * 2)
        self.top_chromosome = [[0] * GENE] * TOP_POP
        self.offspring = [[0] * GENE] * (POP_SIZE - TOP_POP)

        self.gen = 1
        self.killed = 0
        self.nextGenDur = 30

        self.dinos = []

        self.font = pygame.font.SysFont('comicsansms', 24)
        self.gen_string = str(self.gen)
        self.gen_text = self.font.render(self.gen_string, True, (0, 0, 0))

        for i in range(POP_SIZE):
            dino = Dino()
            collision = False
            # [dino, collision, action, duckCountdown, dead_score]
            self.dinos.append([dino, collision, 0, 0, 0])

    def init_array(self):
        # Gene = [probJump_obs1(rock), probJump_obs2(plant), probJump_obs3(birdLo), probJump_obs4(birdMed), probJump_obs5(birdHi),
        #       probDuck_obs1(rock), probDuck_obs2(plant), probDuck_obs3(birdLo), probDuck_obs4(birdMed), probDuck_obs5(birdHi),
        #       probIdle_obs1(rock), probIdle_obs2(plant), probIdle_obs3(birdLo), probIdle_obs4(birdMed), probIdle_obs5(birdHi),
        #       duckDur, duckDurStd, distObs, distObsStd]
        for i in range(len(chromosome)):
            chromosome[i] = random.sample(range(1, 1000), GENE)


    def display(self):
        for i in range(len(chromosome)):
            print(chromosome[i])

    def isItEnd(self):
        self.killed = 0
        for dino in self.dinos:
            if dino[1]:
                self.killed += 1

        if self.killed == POP_SIZE:
            self.nextGenDur = 30

            self.plot_x.append(self.gen)
            self.plot_y1.append(self.avg_score)
            self.plot_y2.append(self.top_score)

            return True
        else:
            return False

    def goToNextGen(self):
        self.fitness_func()
        self.selection()
        self.crossover()
        self.mutation()
        self.evaluation()

        self.avg_score = self.total_score/POP_SIZE

        self.total_score = 0
        self.fitness_sum = 0
        for dino in self.dinos:
            dino[1] = False
            dino[4] = 0

        self.gen += 1
        self.font = pygame.font.SysFont('comicsansms', 24)
        self.gen_string = str(self.gen)
        self.gen_text = self.font.render(self.gen_string, True, (0, 0, 0))

        print("\nGen ", self.gen)
        self.display()

    def action(self, dino, obstacle, c, curr_action, curr_dur):
        #return action value 0=NONE, 1=JUMP, 2=DUCK, 3=ONGOING
        # conversion
        for i in range(len(chromosome[c])):
            if i == 15:
                duck_dur = round(chromosome[c][i] / 10)
            elif i == 17:
                dist_obs = round(chromosome[c][i])
            elif i == 16:
                duck_std = round(chromosome[c][i] / 100)
            elif i == 18:
                dist_std = round(chromosome[c][i] / 10)

        # Duck
        duckDurStd = random.randint(0, duck_std) - round(duck_std/2)
        duckDur = duck_dur + duckDurStd

        # Observe Obstacle
        object_type = obstacle.random_obs
        observe = 0
        distance_var = random.randint(0, dist_std) - round(dist_std/2)
        distance = dist_obs + distance_var
        object_x = obstacle.x
        if curr_action == 2:
            observe = object_x - (dino.rect.x+32)
        else:
            observe = object_x - (dino.rect.x + (16*ratio))

        if (0 <= observe <= distance) and curr_action == 0:
            action_likely = random.random()
            if object_type == 0:
                jump = chromosome[c][0] / (chromosome[c][0] + chromosome[c][5] + chromosome[c][10])
                duck = chromosome[c][5] / (chromosome[c][0] + chromosome[c][5] + chromosome[c][10])
                if action_likely < jump:
                    return 1
                elif action_likely < jump+duck:
                    return 2000+duckDur
                else:
                    return 0
            elif object_type == 1:
                jump = chromosome[c][1] / (chromosome[c][1] + chromosome[c][6] + chromosome[c][11])
                duck = chromosome[c][6] / (chromosome[c][1] + chromosome[c][6] + chromosome[c][11])
                if action_likely < jump:
                    return 1
                elif action_likely < jump+duck:
                    return 2000+duckDur
                else:
                    return 0
            elif object_type == 2:
                jump = chromosome[c][2] / (chromosome[c][2] + chromosome[c][7] + chromosome[c][12])
                duck = chromosome[c][7] / (chromosome[c][2] + chromosome[c][7] + chromosome[c][12])
                if action_likely < jump:
                    return 1
                elif action_likely < jump+duck:
                    return 2000+duckDur
                else:
                    return 0
            elif object_type == 3:
                jump = chromosome[c][3] / (chromosome[c][3] + chromosome[c][8] + chromosome[c][13])
                duck = chromosome[c][8] / (chromosome[c][3] + chromosome[c][8] + chromosome[c][13])
                if action_likely < jump:
                    return 1
                elif action_likely < jump+duck:
                    return 2000+duckDur
                else:
                    return 0
            elif object_type == 4:
                jump = chromosome[c][4] / (chromosome[c][4] + chromosome[c][9] + chromosome[c][14])
                duck = chromosome[c][9] / (chromosome[c][4] + chromosome[c][9] + chromosome[c][14])
                if action_likely < jump:
                    return 1
                elif action_likely < jump+duck:
                    return 2000+duckDur
                else:
                    return 0
        else:
            return curr_action

    def fitness_func(self):
        # apply fitness function
        for i in range(len(self.fitness)):
            self.fitness[i] = round(math.pow(self.dinos[i][4], 1.1)/100)
            self.fitness_sum += self.fitness[i]

        # search top chromosome
        for i in range(len(self.top_chromosome)):
            top = 0
            for j in range(len(self.fitness)):
                if top < self.fitness[j]:
                    top = j
            self.top_chromosome[i] = chromosome[top]

        # convert to prob, [1] < [2] < [3] < ... < [n]
        temp = 0
        for i in range(len(self.fitness)):
            temp += self.fitness[i]
            self.fitness[i] = temp/self.fitness_sum

    def selection(self):
        # wheel selection
        choose_prob = 0
        curr_prop = 0

        # pair of select_parent array
        for i in range(len(self.select_parent)):
            pair_1 = -1
            while True:
                #pair 1
                if i % 2 == 0:
                    choose_prob = random.random()
                    for j in range(len(self.fitness)):
                        invert = (len(self.fitness) - 1) - j
                        if choose_prob < self.fitness[invert]:
                            self.select_parent[i] = chromosome[invert]
                            pair_1 = invert
                    break

                #pair 2
                else:
                    choose_prob = random.random()
                    for j in range(len(self.fitness)):
                        invert = (len(self.fitness) - 1) - j
                        if choose_prob < self.fitness[invert]:
                            self.select_parent[i] = chromosome[invert]
                    if i != pair_1:
                        break
        #print("")
        #print("Parent")
        #for i in range(len(self.select_parent)):
        #    print(self.select_parent[i])

    def crossover(self):
        for i in range(len(self.offspring)):
            random_pair = random.randint(0, NUM_PARENT - 1) * 2
            cross_point = random.randint(1, GENE - 1)
            offspring = [0] * GENE
            for j in range(len(self.offspring[i])):
                if j < cross_point:
                    offspring[j] = self.select_parent[random_pair][j]
                else:
                    offspring[j] = self.select_parent[random_pair + 1][j]
            self.offspring[i] = offspring
        #print("")
        #print("Crossover")
        #for i in range(len(self.offspring)):
        #    print(self.offspring[i])

    def mutation(self):
        #SWAP MUTATION
        for i in range(len(self.offspring)):
            prob_mutate = random.random()
            if prob_mutate < MUTATE_RATE:
                target = random.randint(0, GENE - 1)
                value = random.randint(0, 1000)
                self.offspring[i][target] = value

                # target_1 = random.randint(0, GENE - 1)
                # target_2 = 0
                # while target_1 == target_2:
                #     target_2 = random.randint(0, GENE - 1)

                # temp = self.offspring[i][target_2]
                # self.offspring[i][target_2] = self.offspring[i][target_1]
                # self.offspring[i][target_1] = temp
        #print("")
        #print("Mutation")
        #for i in range(len(self.offspring)):
        #    print(self.offspring[i])

    def evaluation(self):
        global chromosome
        new_chromosome = [[(int)] * GENE] * POP_SIZE
        offspring = POP_SIZE - TOP_POP
        for i in range(len(new_chromosome)):
            if i < offspring:
                new_chromosome[i] = self.offspring[i]
            else:
                top = i-offspring
                new_chromosome[i] = self.top_chromosome[top]
        chromosome = new_chromosome

    def plot_table(self):
        data = {"gen":self.plot_x, "avg_score":self.plot_y1, "top_score":self.plot_y2}
        df = pd.DataFrame(data)

        plt.plot(df["gen"], df["avg_score"], label = "Average Score", color = "mediumblue")
        plt.plot(df["gen"], df["top_score"], label = "Top Score", color = "r")
        plt.ylabel(f"Score")
        plt.xlabel(f"Generation")

        plt.legend()
        plt.show()


def main():
    global score_speed, speed_x, curr_fps
    score = 0
    display_score = "Score: " + str(score)

    # Initialise screen
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Dino Game')
    canvas = screen_width, screen_height
    screen = pygame.display.set_mode(canvas)
    font = pygame.font.SysFont('comicsansms', 24)
    text = font.render(display_score, True, (0, 0, 0))

    # Fill background
    sky_color = 0, 191, 255
    origin = 0, 0
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(sky_color)

    # Others
    setting = Setting()
    ai = AIntelligence()
    ai.init_array()
    ai.display()
    framerate = pygame.time.Clock()
    movement_optimize = 0

    grass_x = [0] * 17
    for i in range(len(grass_x)):
        grass_x[i] = i/15*screen_width

    # init sprites
    dino = Dino()
    obstacle = Obstacle()
    grasses = []
    for i in range(len(grass_x)):
        grass = Grass(grass_x[i])
        grasses.append(grass)

    pygame.key.set_repeat(1)
    while 1:
        time_start = time.time()
        framerate.tick(setting.fps)

        if pygame.mouse.get_pressed() == (1, 0, 0):
            setting.click(mouse_pos)
        elif pygame.mouse.get_pressed() == (0, 0, 0):
            setting.maintain = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if ai_mechanics:
                    ai.plot_table()

                pygame.quit()
                sys.exit()

            if not pause and not ai_mechanics:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # print("UP")
                        dino.jumps()

                    if event.key == pygame.K_DOWN and not obstacle.collision:
                        # print("UP")
                        dino.crawls()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN and not obstacle.collision:
                        # print("UP")
                        dino.uncrawl()

        if (pygame.key.get_pressed()[K_UP] and not pause) and not ai_mechanics:
            # print("UP")
            if obstacle.collision:
                obstacle.reset()
                score = 0
                gameover_timeout = 0

        #Mouse Movement
        mouse_pos = pygame.mouse.get_pos()
        setting.hover_setting(mouse_pos)
        setting.hover_text(mouse_pos)

        if ai_mechanics:
            if not pause:
                if not obstacle.collision:
                    c = 0
                    obstacle.incoming(setting.fps)
                    for one_dino in ai.dinos:
                        one_dino[2] = ai.action(one_dino[0], obstacle, c, one_dino[2], one_dino[3])
                        if one_dino[2] == 1:
                            one_dino[0].jumps()
                            one_dino[2] = 3
                        elif one_dino[2] > 2000 and not one_dino[0].jump:
                            one_dino[3] = one_dino[2]%2000
                            one_dino[2] = 3
                            one_dino[0].crawls()
                        elif one_dino[2] == 3 and one_dino[0].on_ground:
                            one_dino[2] = 0

                        if one_dino[3] > 0:
                            one_dino[3] -= 1
                        elif one_dino[3] <= 0:
                            one_dino[0].uncrawl()
                            one_dino[3] = 0
                            one_dino[2] = 0

                        if not one_dino[1]:
                            one_dino[1] = pygame.Rect.colliderect(one_dino[0].rect, obstacle.hitbox)
                            if one_dino[1]:
                                one_dino[4] = score
                                ai.total_score += score
                                ai.top_score = score

                        obstacle.collision = ai.isItEnd()
                        one_dino[0].forward()
                        c += 1

                    if movement_optimize >= 1 / 65:
                        movement_optimize = 0
                        for one_dino in ai.dinos:
                            fall(one_dino[0], grasses)
                            one_dino[0].jumping()

                    score += setting.score_modifier
                    score_speed = math.floor(score / 10) + 1
                    speed_x = 120.0 * ((score_speed ** (1 / 7)) + 0.25) / setting.fps
                    display_score = "Score: " + str(round(score))
                    text = font.render(display_score, True, (0, 0, 0))

                    # update frames
                    screen.blit(background, origin)

                    # grass update
                    curr_w_terrain = width_terrain()
                    for grass in grasses:
                        grass.forward(curr_w_terrain)
                        screen.blit(grass.image, grass.rect.topleft)
                else:
                    if ai.nextGenDur > 0:
                        ai.nextGenDur -= 1
                    else:
                        ai.goToNextGen()
                        obstacle.reset()
                        score = 0

                    obstacle.incoming(setting.fps)
                    # update frames
                    screen.blit(background, origin)

                    # grass update
                    for grass in grasses:
                        grass.forward(curr_w_terrain)
                        screen.blit(grass.image, grass.rect.topleft)
            else:
                # update frames
                screen.blit(background, origin)

                # grass update
                for grass in grasses:
                    screen.blit(grass.image, grass.rect.topleft)

            for one_dino in ai.dinos:
                if not one_dino[1]:
                    screen.blit(one_dino[0].image, one_dino[0].rect.topleft)

            screen.blit(obstacle.image, obstacle.rect.topleft)
            screen.blit(text, (10, 10))
            screen.blit(ai.gen_text, (screen_width - 96, 0))
        else:
            if not pause:
                if not obstacle.collision:
                    dino.forward()

                    if movement_optimize >= 1 / 65:
                        movement_optimize = 0
                        fall(dino, grasses)
                        dino.jumping()

                    obstacle.incoming(setting.fps)
                    obstacle.collision = pygame.Rect.colliderect(dino.rect, obstacle.hitbox)

                    score += setting.score_modifier
                    score_speed = math.floor(score / 100) + 1
                    speed_x = 120.0 * ((score_speed ** (1 / 7)) + 0.25) / setting.fps
                    display_score = "Score: " + str(round(score))
                    text = font.render(display_score, True, (0, 0, 0))

                    # update frames
                    screen.blit(background, origin)

                    # grass update
                    curr_w_terrain = width_terrain()
                    for grass in grasses:
                        grass.forward(curr_w_terrain)
                        screen.blit(grass.image, grass.rect.topleft)
                else:
                    # update frames
                    screen.blit(background, origin)

                    # grass update
                    for grass in grasses:
                        screen.blit(grass.image, grass.rect.topleft)
            else:
                # update frames
                screen.blit(background, origin)

                # grass update
                for grass in grasses:
                    screen.blit(grass.image, grass.rect.topleft)

            screen.blit(dino.image, dino.rect.topleft)
            screen.blit(obstacle.image, obstacle.rect.topleft)
            screen.blit(text, (10, 10))

        screen.blit(setting.img, (setting.pos_x, setting.pos_y))

        if setting.setting_visible:
            screen.blit(setting.menu, setting.menu_pos)
            setting_center_width = (screen_width/2) - (setting.name_display.get_rect()[2]/2)
            screen.blit(setting.name_display, (setting_center_width, setting.center_height - 70))
            screen.blit(setting.fps_display, (setting.center_width, setting.center_height-10))
            screen.blit(setting.ai, (setting.center_width, setting.center_height + 30))

        pygame.display.flip()
        curr_fps = 1.0 / (time.time() - time_start)
        movement_optimize += time.time() - time_start
        setting.optimize_perf()
        # print("FPS: ", curr_fps)


if __name__ == "__main__":
    main()
