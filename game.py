import shelve
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

    def update(self,screen: pg.Surface):
        screen.blit(self.img, [WIDTH/2,HEIGHT/2])


class Score:
    """
    取得コインに対応するスコアを表示するクラス
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)
        self.color = (0, 0, 0)
        self.score = 0
        self.image = self.font.render(f"Score: {self.score}", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = 100, 50  

    def score_up(self, add): #スコアを増やす関数
        self.score += add

    def update(self, screen: pg.Surface): #スコアを更新、表示する関数
        if 100<self.score<500:
            self.font=pg.font.Font(None, 55)
            self.color=(80,0,0)
        elif 500<=self.score<1000:
            self.font=pg.font.Font(None, 60)
            self.color=(160,0,0)
        elif 1000<=self.score:
            self.font=pg.font.Font(None, 65)
            self.color=(255,0,0)
        self.image = self.font.render(f"Score: {self.score}", 0,self.color)
        screen.blit(self.image,self.rect)
    




def main():
    pg.display.set_caption("gmae")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img_2=pg.transform.flip(bg_img,True,False)
    hito = Hito()
    coins = pg.sprite.Group()
    score = Score()
    
    tmr = 0
    x = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[1600-x,0])
        screen.blit(bg_img,[3200-x,0])
       # for i in pg.sprite.spritecollide(hito,coins,True): #コインとぶつかったらスコアを1増やす
        score.score=10*len(pg.sprite.spritecollide(hito,coins,True))
        score.update(screen)

        


        hito.update(screen)

        pg.display.update()
        tmr += 1 


        
        
        

        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()