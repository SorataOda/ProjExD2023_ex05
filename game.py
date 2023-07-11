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
        初期化メゾット
        """
        self.img=pg.image.load("ex05/fig/hito1.png")
        self.img = pg.transform.rotozoom(self.img,0,0.25)
        self.img=pg.transform.flip(self.img,True,False)
        self.rect = self.img.get_rect()
        self.type = "run"
        self.janptop = -300
        self.janp = 0

    def update(self,screen: pg.Surface):
        """
        updateメゾット
        self.typeを3つにわけ、ジャンプを表現
        """
        if self.type == "janpup":
            self.janp -= 10
        if self.janp < self.janptop:
            self.type ="janpdown"
        if self.type == "janpdown":
            self.janp += 10
            if self.janp == 0:
                self.type = "run"
            
        screen.blit(self.img, [WIDTH/4,HEIGHT/2+100+self.janp])


def main():
    pg.display.set_caption("gmae")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img_2=pg.transform.flip(bg_img,True,False)
    yuka = pg.image.load("ex05/fig/renga.png")
    rect = yuka.get_rect()
    print(rect)
    hito = Hito()
    
    
    tmr = 0
    x = 0
    while True:


        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                hito.type = "janpup"

        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[1600-x,0])
        screen.blit(bg_img,[3200-x,0])
        screen.blit(yuka,[-x,HEIGHT/2+261])
        screen.blit(yuka,[1600-x,HEIGHT/2+261])
        screen.blit(yuka,[3200-x,HEIGHT/2+261])



        


        hito.update(screen)


        pg.display.update()

        tmr += 10
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()