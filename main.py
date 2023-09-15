import pygame as pg
import sys

import pygame.display
from sprites import *
from config import *
import sys

class game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pg.display.set_caption('India to the Moon')
        self.clock = pg.time.Clock()
        self.font = pg.font.Font('PressStart2P-Regular.ttf', 32)
        self.running = True
        self.intro_background = pg.image.load('img/bg.jpg')
        self.go = pg.image.load("img/go.jpg")
        self.timer = 1000
        self.tfont = pg.font.Font('Roboto-Regular.ttf', 20)
        self.q_count = 0
        self.los_i = 0


    def build_map(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                ground(self, j, i)
                if column == "B":
                    block(self,j,i)
                if column == "P":
                    self.Player = Player(self, j, i)
                if column == "T":
                    thing(self, j, i)
                if column == "Q":
                    Quest(self, j, i)




    def new(self):
        self.playing = True

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.crati=  pg.sprite.LayeredUpdates()
        self.obs = pg.sprite.LayeredUpdates()
        self.hit = pg.sprite.LayeredUpdates()
        self.thing =  pg.sprite.LayeredUpdates()
        self.welcome =  pg.sprite.LayeredUpdates()
        self.q = pg.sprite.LayeredUpdates()
        self.player = pg.sprite.LayeredUpdates()

        self.build_map()


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                self.running = False



    def update(self):
        self.all_sprites.update()
        pygame.display.flip()
        self.timer -= 0.00001
        self.timer = int(self.timer)

        if self.timer <= 0:
            self.timer = 0
            self.game_over()
            self.playing = False

        if self.q_count == 10:
            self.you_win()
            self.playing = False





    def draw(self):
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        timer_text = self.tfont.render(f'Time: {self.timer}', True, black)
        timer_rect = timer_text.get_rect(bottomright=(WIN_WIDTH, WIN_HEIGHT))
        self.screen.blit(timer_text, timer_rect)
        q_text = self.tfont.render(f'Found: {self.q_count}/10', True, black)
        q_rect = q_text.get_rect(bottomleft=(0, WIN_HEIGHT))
        self.screen.blit(q_text, q_rect)
        fact_text = self.tfont.render(list_of_stuff[self.los_i], True, black)
        fact_rect = fact_text.get_rect()
        fact_rect.bottom = WIN_HEIGHT  # Set the bottom of the rect to the window's height
        fact_rect.centerx = WIN_WIDTH/2

        self.screen.blit(fact_text, fact_rect)


        self.clock.tick(FPS)
        pg.display.update()




    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()



    def game_over(self):
        text = self.font.render('Game Over', True, white)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = button(10, 50, 350, 50, white, black, 'Play Again', 32)
        photo_button = button(10, 50, 200, 50, white, black, 'Launch Photobooth', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)

            self.clock.tick(FPS)
            pg.display.update()

    def you_win(self):
        text = self.font.render('You Win', True, white)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))


        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()


            self.screen.blit(self.go, (0,0))
            self.screen.blit(text, text_rect)

            self.clock.tick(FPS)
            pg.display.update()


    def intro_screen(self):
        intro = True
        title = self.font.render('India to the Moon', True, white)

        title_rect = title.get_rect(x=10, y=10)
        play_button = button(10, 50, 200, 50, white, black, 'play', 32)

        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                    intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pg.display.update()








game = game()
game.intro_screen()
game.new()

while game.running:
    game.main()
    game.game_over()

pygame.quit()
sys.exit()
