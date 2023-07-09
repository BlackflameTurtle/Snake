import sys
import pygame
import pygame.font
from pygame.locals import *
import random
import time
pygame.init()
screen_x = 690
screen_y = 540
dimensions = 30
background = (173, 216, 230)
green = pygame.image.load(("Modelsandmusic/Green block.jpg"))
blue = pygame.image.load(("Modelsandmusic/blue snake.jpg"))
red = pygame.image.load(("Modelsandmusic/red.jpg"))
purple = pygame.image.load(("Modelsandmusic/purple.jpg"))
colors = [green, blue, red, purple]

#All attributes of the gold apple
class Golden_Apple:
    def __init__(self, background):
        self.golden_apple = pygame.image.load("modelsandmusic/golden apple.jpg").convert_alpha(background)
        self.background = background
        self.golden_apple_x = dimensions * 30
        self.golden_apple_y = dimensions * 30
    def golden_appearance(self):
        self.background.blit(self.golden_apple, (self.golden_apple_x, self.golden_apple_y))
        pygame.display.flip()
    def golden_movement(self):
        self.golden_apple_x = random.randint(0, screen_x *3/dimensions) * dimensions
        self.golden_apple_y = random.randint(0, screen_y *3/dimensions) * dimensions


#all apple attributes
class Apple:
    def __init__(self, background):
        self.apple = pygame.image.load("modelsandmusic/apple.jpg").convert()
        self.background = background
        self.apple_x = dimensions * 12
        self.apple_y = dimensions * 12
    def make_apple_appear(self):
        self.background.blit(self.apple, (self.apple_x, self.apple_y))

    #random apple movement
    def apple_movement (self):
        self.apple_x = random.randint(0, screen_x/dimensions - 1) * dimensions
        self.apple_y = random.randint(0, (screen_y/dimensions - 1)) * dimensions

#Everything that makes the snake exist
class Snake:
    def __init__(self, background_screen, length):
        self.color_num = 0
        self.score1 = -3
        self.length = length
        self.background_screen = background_screen
        self.square = colors[self.color_num]
        self.block_y = [dimensions] * length
        self.block_x = [dimensions] * length
        self.direction = "down"
        self.picture = pygame.image.load("Modelsandmusic/background.jpg")
    def make_appear(self):
        self.background_screen.fill(background)
        #self.background_screen.blit(self.picture, (0,0))
        for part_of_snake in range(self.length):
            self.background_screen.blit(self.square, (self.block_x[part_of_snake], self.block_y[part_of_snake]))



    #increasing length and score when eating apples
    def apple_make_snake_tall(self):
        self.length += 1
        self.block_x.append(1)
        self.block_y.append(1)
    def gold_make_score_go(self):
        self.score1 += 3
        self.length += 1
        self.block_x.append(1)
        self.block_y.append(1)



    #diretion of movement
    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_right(self):
        self.direction = "right"

    def move_left(self):
        self.direction = "left"
    #tells each part of snake where to go while moving
    def infinite_move(self):
        for part_of_snake in range(self.length - 1, 0, -1):
            self.block_x[part_of_snake] = self.block_x[part_of_snake - 1]
            self.block_y[part_of_snake] = self.block_y[part_of_snake - 1]

        #movement of head
        if self.direction == "up":
            self.block_y[0] -= dimensions
        if self.direction == "down":
            self.block_y[0] += dimensions
        if self.direction == "right":
            self.block_x[0] += dimensions
        if self.direction == "left":
            self.block_x[0] -= dimensions
        if self.direction == "none":
            self.block_x = self.block_x
            self.block_y = self.block_y
        #snake appears
        self.make_appear()

#Where everything goes to actually happen
class Game:
    def __init__(self):
        pygame.mixer.init
        self.music()
        self.surface = pygame.display.set_mode((screen_x, screen_y))
        self.surface.fill(background)
        self.snake = Snake(self.surface, 3)
        self.snake.make_appear()
        self.apple = Apple(self.surface)
        self.apple.make_apple_appear()
        self.golden = Golden_Apple(self.surface)
        self.golden.golden_appearance()


#General collision logic(applied for apples and game over conditons)
    def collide(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 :
            if y1 >= y2 and y1 <= y2:
                return True
        return False
    #removed feature
    def color(self):
        running = True
        while running:
            for x in pygame.event.get():
                if x.type == KEYDOWN:
                    if x.key == K_c:
                        self.snake.color_num += 1
                        self.snake.square = colors[self.snake.color_num]

#displays score
    def score(self):
        font = pygame.font.SysFont('Britannic', 24, bold=False, italic=False)
        score = font.render(f"Score: {self.snake.length + self.snake.score1}", True, (255, 255, 255))
        self.surface.blit(score, (screen_x/2 -25, 10))
    def music(self):
        pygame.mixer.music.load("Modelsandmusic/music.mp3")
        pygame.mixer.music.play(-1)
#color swap upon reaching certain scores
    def upgrade(self):
        if self.snake.length + self.snake.score1 == 10:
            self.snake.square = colors[3]
        if self.snake.length + self.snake.score1 == 11:
            self.snake.square = colors[3]
        if self.snake.length + self.snake.score1 == 12:
            self.snake.square = colors[3]
        if self.snake.length + self.snake.score1 == 13:
            self.snake.square = colors[3]
        if self.snake.length + self.snake.score1 >= 30:
            self.snake.square = colors[1]
        if self.snake.length + self.snake.score1 >= 60:
            self.snake.square = colors[2]


#called at the end of the game for the game to function
    def play(self):
        self.snake.infinite_move()
        self.snake.make_appear()
        self.apple.make_apple_appear()
        self.score()
        self.golden.golden_appearance()
        pygame.display.flip()
        self.upgrade()

        #apple collision
        sound = pygame.mixer.Sound("Modelsandmusic/Point.mp3")
        rando = random.randint(0,2)
        if self.collide(self.snake.block_x[0], self.snake.block_y[0], self.apple.apple_x, self.apple.apple_y):
            if 0 <= self.golden.golden_apple_x <= screen_x and 0 <= self.golden.golden_apple_y <= screen_y:
                sound = pygame.mixer.Sound("Modelsandmusic/Point.mp3")
                pygame.mixer.Sound.play(sound)
                self.apple.apple_movement()
                self.snake.apple_make_snake_tall()

            else:
                pygame.mixer.Sound.play(sound)
                self.apple.apple_movement()
                self.snake.apple_make_snake_tall()
                self.golden.golden_movement()

        #gold apple collision
        if self.collide(self.snake.block_x[0], self.snake.block_y[0], self.golden.golden_apple_x, self.golden.golden_apple_y):
            sound = pygame.mixer.Sound("Modelsandmusic/Point.mp3")
            pygame.mixer.Sound.play(sound, 1)
            pygame.mixer.Sound.play(sound, 1)
            self.golden.golden_movement()
            self.snake.gold_make_score_go()

        #All game over logic
        #colliding with yourself
        for b in range(1,self.snake.length):
            if self.collide(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[b], self.snake.block_y[b]):
                crash = pygame.mixer.Sound("Modelsandmusic/Crash.mp3")
                pygame.mixer.Sound.play(crash)
                raise "Game over"
        #Too far to the left or right
        if self.snake.block_x[0] >= (screen_x) or self.snake.block_x[0] <= -1:
            crash = pygame.mixer.Sound("Modelsandmusic/Crash.mp3")
            pygame.mixer.Sound.play(crash)
            raise "Game over"
        #Too far up or down
        if self.snake.block_y[0] >= (screen_y) or self.snake.block_y[0] <= -1:
            crash = pygame.mixer.Sound("Modelsandmusic/Crash.mp3")
            pygame.mixer.Sound.play(crash)
            raise "Game over"

    #Game over screen that shows up when a game over occurs
    def show_game_over(self):
        self.wordcolor1 = 102, 0, 0
        self.wordcolor2 = 102, 0, 0
        self.wordcolor3 = 102, 0, 0
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('Britannic', 50, bold=True, italic=False)
        font1 = pygame.font.SysFont('Britannic', 70, bold=True, italic=False)
        line0 = font1.render("Game Over ", True, (102, 0, 0))
        self.surface.blit(line0, ((screen_x/6 + 50), (screen_y - 500)))
        line1 = font.render(f"Score: {self.snake.length  + self.snake.score1}", True, (102, 0, 0))
        self.surface.blit(line1, ((screen_x/2 - 100), (screen_y - 400)))
        line2 = font.render("Replay", True, (self.wordcolor1))
        line3 = font.render("Title", True, (self.wordcolor2))
        line4 = font.render("Screen", True, (self.wordcolor2))
        line5 = font.render("Quit", True, (self.wordcolor3))
        self.surface.blit(line2, ((30), (325)))
        self.surface.blit(line3, (280, (screen_y - 240)))
        self.surface.blit(line4, (260, (screen_y - 190)))
        self.surface.blit(line5, (515, (screen_y - 215)))


        self.overcolor1 = 255, 0, 0
        self.overcolor2 = 255, 0, 0
        self.overcolor3 = 255, 0, 0

        pygame.draw.rect((self.surface), self.overcolor1,(24, 294, 160, 120), 1, 10)
        pygame.draw.rect((self.surface), self.overcolor2,(255, 294, 160, 120), 1, 10)
        pygame.draw.rect((self.surface), self.overcolor3,(486, 294, 160, 120), 1, 10)
        pygame.display.flip()
        pygame.mixer.music.pause()
    #Refreshes the game over screen when you hover over a different button
    def over_boxes(self):

        pygame.draw.rect((self.surface), (102, 0, 0), (24, 294, 160, 120), 1, 10)
        pygame.draw.rect((self.surface), (102, 0, 0), (255, 294, 160, 120), 1, 10)
        pygame.draw.rect((self.surface), (102, 0, 0), (486, 294, 160, 120), 1, 10)

    #Resets everything before replay
    def reset(self):
        self.snake = Snake(self.surface,3)
        self.apple = Apple(self.surface)
        self.golden = Golden_Apple(self.surface)

    #show title screen - button color change
    def title_screen(self):
        self.color5 = 200, 150, 0
        self.color6 = 200, 150, 0
        self.color7 = 200, 150, 0
        self.color8 = 200, 150, 0
        fill = 1
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 285 <= mouse_x <= 385 and 241 <= mouse_y <= 284:
            self.color5 = (255, 0, 0)
        if 270 <= mouse_x <= 410 and 291 <= mouse_y <= 334:
            self.color7 = (255, 0, 0)
        if 287 <= mouse_x <= 392 and 340 <= mouse_y <= 383:
            self.color6 = (255, 0, 0)
        if 287 <= mouse_x <= 411 and 391 <= mouse_y <= 434:
            self.color8 = (255, 0, 0)
        self.color3 = 0, 0, 0
        self.surface.fill(background)
        picture = pygame.image.load("Modelsandmusic/background.jpg")
        master_y = screen_y - 150
        hard_y = screen_y - 200
        normal_y = screen_y - 250
        self.easy_y = screen_y - 300
        font1 = pygame.font.SysFont('Britannic', 90, bold=True, italic=False)
        line0 = font1.render("Snake", True, (0,0,0))
        font2 = pygame.font.SysFont('Britannic', 30, bold=True, italic=False)
        self.font3 = pygame.font.SysFont('Britannic', 40, bold=True, italic=False)
        self.surface.blit(line0, ((screen_x / 2 - 125), (screen_y - 400)))
        self.line3 = self.font3.render("Easy", True, (self.color3))
        line4 = self.font3.render("Normal", True, (0,0,0))
        line5 = self.font3.render("Hard", True, (0,0,0))
        line6 = self.font3.render("Master", True, (0,0,0))
        self.surface.blit(self.line3, ((screen_x/2 -50), self.easy_y))
        self.surface.blit(line5, ((screen_x/2 - 50), hard_y))
        self.surface.blit(line4, ((screen_x/2 - 70), normal_y))
        self.surface.blit(line6, ((screen_x/2 - 65), master_y))
        snakey = pygame.image.load("Modelsandmusic/snake icon-1.jpg")
        self.surface.blit(snakey, (265, 90))
        pygame.draw.rect(self.surface, (self.color5), (285, 241, 100, 43), fill, 10)
        pygame.draw.rect(self.surface, (self.color6), (287, 340, 105, 43), fill, 10)
        pygame.draw.rect(self.surface, (self.color7), (270, 291, 140, 43), fill, 10)
        pygame.draw.rect(self.surface, (self.color8), (271, 391, 140, 43), fill, 10)
        pygame.display.flip()
    #refreshes pause screen when you float over a new button
    def pause_boxes(self):
        self.colorp1 = 200, 150, 0
        self.colorp2 = 200, 150, 0
        self.colorp3 = 200, 150, 0
        self.colorp4 = 200, 150, 0
        self.colorp5 = 200, 150, 0
        self.colorp6 = 200, 150, 0
        fill = 1

        self.color3 = 0, 0, 0
        picture = pygame.image.load("Modelsandmusic/background.jpg")
        master_y = screen_y - 150
        hard_y = screen_y - 200
        normal_y = screen_y - 250
        self.easy_y = screen_y - 300
        pygame.draw.rect(self.surface, self.colorp1, (285, 241, 100, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp2, (287, 340, 105, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp3, (270, 291, 140, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp4, (271, 391, 140, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp5, (-1, 0, 75, 27), fill, 10)
        pygame.draw.rect(self.surface, self.colorp6, (-1, 30, 67, 27), fill, 10)
    #pause screen appearance but not function
    def pause_screen(self):
        self.colorp1 = 200, 150, 0
        self.colorp2 = 200, 150, 0
        self.colorp3 = 200, 150, 0
        self.colorp4 = 200, 150, 0
        self.colorp5 = 200, 150, 0
        self.colorp6 = 200, 150, 0
        fill = 1

        self.color3 = 0, 0, 0
        picture = pygame.image.load("Modelsandmusic/background.jpg")
        master_y = screen_y - 150
        hard_y = screen_y - 200
        normal_y = screen_y - 250
        self.easy_y = screen_y - 300
        font1 = pygame.font.SysFont('Britannic', 70, bold=True, italic=False)
        line0 = font1.render("Paused", True, (255, 255, 255))
        self.font2 = pygame.font.SysFont('Britannic', 20, bold=True, italic=False)
        self.font3 = pygame.font.SysFont('Britannic', 40, bold=True, italic=False)
        self.surface.blit(line0, ((screen_x / 2 - 125), (20)))
        self.line3 = self.font3.render("Easy", True, (0, 0, 0))
        line4 = self.font3.render("Normal", True, (0, 0, 0))
        line5 = self.font3.render("Hard", True, (0, 0, 0))
        line6 = self.font3.render("Master", True, (0, 0, 0))
        line7 = self.font2.render("Restart", True, (0, 0, 0))
        line8 = self.font2.render("Quit", True, (0, 0, 0))
        self.surface.blit(self.line3, ((screen_x / 2 - 50), self.easy_y))
        self.surface.blit(line5, ((screen_x / 2 - 50), hard_y))
        self.surface.blit(line4, ((screen_x / 2 - 70), normal_y))
        self.surface.blit(line6, ((screen_x / 2 - 65), master_y))
        self.surface.blit(line7, ((2), 1))
        self.surface.blit(line8, ((10), 30))
        pygame.draw.rect(self.surface, self.colorp1, (285, 241, 100, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp2, (287, 340, 105, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp3, (270, 291, 140, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp4, (271, 391, 140, 43), fill, 10)
        pygame.draw.rect(self.surface, self.colorp5, (-1, 0, 75, 27), fill, 10)
        pygame.draw.rect(self.surface, self.colorp6, (-1, 30, 67, 27), fill, 10)



    #title screen functionality
    def title(self):
        self.speed = 0.07
        running = True
        play = False
        quit = False
        while not play and running and not quit:
            self.title_screen()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                mouse_x, mouse_y = pygame.mouse.get_pos()


                if pygame.mouse.get_pressed() != (0,0,0):
                    if 285 <= mouse_x <= 385 and 241 <= mouse_y <= 284:
                        self.speed = 0.15
                        running = False
                    if 270 <= mouse_x <= 410 and 291 <= mouse_y <= 334:
                        self.speed = 0.12
                        running = False
                    if 287 <= mouse_x <= 392 and 340 <= mouse_y <= 383:
                        self.speed = 0.09
                        running = False
                    if 287 <= mouse_x <= 411 and 391 <= mouse_y <= 434:
                        self.speed = 0.06
                        running = False



    #Controls\main game loop
    def run(self):
        menu = False
        running = True
        pause = False
        quit = False
        while running and not quit:
            for event in pygame.event.get():
                #Get out of app
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    #Pause and unpause
                    #elif event.key == K_RETURN:
                        #if pause and not menu :
                            #if self.snake.direction == "up":
                             #   self.snake.move_right()
                              #  pygame.mixer.music.unpause()
                               # pause = False
                            #else:
                             #   self.snake.move_down()
                              #  pygame.mixer.music.unpause()
                               # pause = False
                        #if pause and menu:
                         #   pygame.mixer.music.unpause()
                          #  pause = False

                    elif event.key == K_SPACE:
                        if pause == False:
                            pause = True
                            running = True
                            menu = True
                            self.pause_screen()
                            pygame.display.flip()





                    elif event.key == K_e:
                        self.snake.length = self.snake.length - 1
                        self.snake.score1 = self.snake.score1 + 1
                        self.score()
                        pygame.display.flip()
                        cheat = pygame.mixer.Sound("Modelsandmusic/bloop.mp3")
                        pygame.mixer.Sound.play(cheat)
                    elif event.key == K_q:
                        self.snake.score1 = self.snake.score1 + 1
                        self.score()
                        pygame.display.flip()
                        cheat = pygame.mixer.Sound("Modelsandmusic/bloop.mp3")
                        pygame.mixer.Sound.play(cheat)


                    #Controls
                    elif event.key == K_w:
                        self.snake.move_up()
                    elif event.key == K_s:
                        self.snake.move_down()
                    elif event.key == K_d:
                        self.snake.move_right()
                    elif event.key == K_a:
                        self.snake.move_left()
                    elif event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    elif event.key == K_LEFT:
                        self.snake.move_left()


            mouse_x, mouse_y = pygame.mouse.get_pos()
            #pause menu buttons functionality
            if pause and menu:
                if pygame.mouse.get_pressed() != (0, 0, 0):
                    if 285 <= mouse_x <= 385 and 241 <= mouse_y <= 284:
                        self.speed = 0.16
                        pause = False
                    if 270 <= mouse_x <= 410 and 291 <= mouse_y <= 334:
                        self.speed = 0.13
                        pause= False
                    if 287 <= mouse_x <= 392 and 340 <= mouse_y <= 383:
                        self.speed = 0.1
                        pause = False
                    if 287 <= mouse_x <= 411 and 391 <= mouse_y <= 434:
                        self.speed = 0.06
                        pause = False
                    if 0 <= mouse_x <= 75 and 0 <= mouse_y <= 27:
                        self.reset()
                        pause = False
                    if 0 <= mouse_x <= 66 and 30 <= mouse_y <= 57:
                        pygame.quit()
                        sys.exit()
                if 285 <= mouse_x <= 385 and 241 <= mouse_y <= 284:
                    self.pause_boxes()
                    self.colorp1 = (255, 0, 0)
                    pygame.draw.rect(self.surface, (self.colorp1), (285, 241, 100, 43), 1, 10)
                    pygame.display.flip()
                if 287 <= mouse_x <= 392 and 340 <= mouse_y <= 383:
                    self.pause_boxes()
                    self.colorp2 = (255, 0, 0)
                    pygame.draw.rect(self.surface, self.colorp2, (287, 340, 105, 43), 1, 10)
                    pygame.display.flip()
                if 270 <= mouse_x <= 410 and 291 <= mouse_y <= 334:
                    self.pause_boxes()
                    self.colorp3 = (255, 0, 0)
                    pygame.draw.rect(self.surface, self.colorp3, (270, 291, 140, 43), 1, 10)
                    pygame.display.flip()
                if 287 <= mouse_x <= 411 and 391 <= mouse_y <= 434:
                    self.pause_boxes()
                    self.colorp4 = (255, 0, 0)
                    pygame.draw.rect(self.surface, (self.colorp4), (271, 391, 140, 43), 1, 10)
                    pygame.display.flip()

                if 0 <= mouse_x <= 75 and 0 <= mouse_y <= 27:
                    self.pause_boxes()
                    self.colorp5 = (255, 0, 0)
                    pygame.draw.rect(self.surface, self.colorp5, (-1, 0, 75, 27), 1, 10)
                    pygame.display.flip()
                if 0 <= mouse_x <= 66 and 30 <= mouse_y <= 57:
                    self.pause_boxes()
                    self.colorp6 = (255, 0, 0)
                    pygame.draw.rect(self.surface, self.colorp6, (-1, 30, 67, 27), 1, 10)
                    pygame.display.flip()

            #game over button functionality
            if pause and not menu:
                if pygame.mouse.get_pressed() != (0, 0, 0):
                    if 24 <= mouse_x <= 184 and 294 <= mouse_y <= 414:
                        if self.snake.direction == "up":
                            self.snake.move_right()
                            pygame.mixer.music.unpause()
                            pause = False
                        else:
                            self.snake.move_down()
                            pygame.mixer.music.unpause()
                            pause = False
                    if 255 <= mouse_x <= 415 and 294 <= mouse_y <= 414:
                        pause = False
                        pygame.mixer.music.unpause()
                        self.reset()
                        self.title()
                    if 486 <= mouse_x <= 646 and 294 <= mouse_y <= 414:
                        pygame.quit()
                        sys.exit()
                if 24 <= mouse_x <= 184 and 294 <= mouse_y <= 414:
                    self.over_boxes()
                    self.overcolor1 = 255, 255, 255
                    pygame.draw.rect((self.surface), self.overcolor1, (24, 294, 160, 120), 1, 10)
                    pygame.display.flip()
                if 255 <= mouse_x <= 415 and 294 <= mouse_y <= 414:
                    self.over_boxes()
                    self.overcolor2 = 255, 255, 255
                    pygame.draw.rect((self.surface), self.overcolor2, (255, 294, 160, 120), 1, 10)
                    pygame.display.flip()
                if 486 <= mouse_x <= 646 and 294 <= mouse_y <= 414:
                    self.over_boxes()
                    self.overcolor3 = 255, 255, 255
                    pygame.draw.rect((self.surface), self.overcolor3, (486, 294, 160, 120), 1, 10)
                    pygame.display.flip()


            #stopping the game for game over
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                menu = False
                self.reset()
            #interval between inputs\speed of movement
            time.sleep(self.speed)



#calls game to make everything happen
if __name__ == "__main__":
    game = Game()
    game.title()
    game.run()











