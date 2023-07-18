import sys
from typing import Any
import pygame as pg
from pygame.sprite import AbstractGroup


WIDTH = 1600
HEIGHT = 900

class Hito(pg.sprite.Sprite):
    """
    操作する人に関するクラス
    """

    def __init__(self):
        """
        """
        self.img=pg.image.load("ex05/fig/hito1.png")
        self.img = pg.transform.rotozoom(self.img,0,0.25)
        self.img=pg.transform.flip(self.img,True,False)
        self.rect = self.img.get_rect()
        self.state = "normal"
        self.hyper_life = -1


    def change_img(self,screen: pg.Surface):
        self.img = pg.transform.rotozoom(pg.image.load(f"ex05/fig/UC.NTD.png"),0,1.0)
        self.rect = self.img.get_rect()
        self.rect.center = 83, 300

    def change_state(self,state:str,hyper_life:int):
        self.state = state
        self.hyper_life = hyper_life

    def update(self,screen: pg.Surface):
        if self.state == "hyper":
            self.hyper_life -= 1

        if self.hyper_life < 0:
            self.change_state("normal", -1)
            self.img=pg.image.load("ex05/fig/hito1.png")
            self.img = pg.transform.rotozoom(self.img,0,0.25)
            self.img=pg.transform.flip(self.img,True,False)
            self.rect = self.img.get_rect()
        screen.blit(self.img, [WIDTH/2,HEIGHT/2])




def main():
    pg.display.set_caption("gmae")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    score = Score()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img_2=pg.transform.flip(bg_img,True,False)
    hito = Hito()
    
    
    tmr = 0
    x = 0
    while True:


        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0
            if event.type == pg.KEYDOWN and event.key == pg.K_LSHIFT:
                if score.score >= 0:
                    hito.change_state("hyper",600)
                    hito.change_img(screen)
        print(hito.hyper_life)

        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[1600-x,0])
        screen.blit(bg_img,[3200-x,0])

        


        hito.update(screen)

        pg.display.update()
        tmr += 1 

        clock.tick(60)

class Score:
    def __init__(self):
        self.score = 0



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()