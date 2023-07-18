import random
import sys
import time
from typing import Any
import pygame as pg
from pygame.sprite import AbstractGroup


WIDTH = 1600
HEIGHT = 900

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト hito SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.rect.left < 0 :  # 横方向のはみ出し判定
        yoko = False
    if obj.rect.top < 0 or HEIGHT < obj.rect.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

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
        self.rect.center = WIDTH/2,(HEIGHT/2)+165
        self.type = "run"
        self.janptop = -20
        self.janp = 0        
        self.item = False
        self.vx = -1
        self.item_life = 0

    def item_use(self,life: int):
        self.item = True
        self.item_life = 500

    def change_img(self,name: str ,screen:pg.Surface):
        """
        主人公の画像を差し替えるメゾット
        引数1：name　ファイル名.拡張子
        引数2：screen
        """
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/{name}"), 0, 0.5)
        screen.blit(self.image, self.rect)

    

    def update(self,screen: pg.Surface):
        """
        updateメゾット
        self.typeを3つにわけ、ジャンプを表現
        """
        if self.type == "janpup":
            self.janp -= 1
            if self.janp < self.janptop:
                self.type ="janpdown"
                self.janp = 0
        elif self.type == "janpdown":
            self.janp += 1
            if self.rect.centery >= (HEIGHT/2)+165 :
                self.type = "run"
                self.janp = 0
        if self.item == True:
            if self.rect.centerx > WIDTH:
                self.rect.move_ip(0,+self.janp)
            else:
                self.rect.move_ip(+2, +self.janp)
            self.item_life -= 1
            if self.item_life == 0:
                self.item = False
        if self.item == False:
            self.rect.move_ip(-1,+self.janp)

            
        screen.blit(self.img, self.rect)


class Item(pg.sprite.Sprite):
    """
    アイテムに関するクラス
    """
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("ex05/fig/item.png")
        self.image = pg.transform.rotozoom(self.image,-10,0.1)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH,random.randint((HEIGHT/2-200),HEIGHT/2+200)
        self.vx = -6
        self.use = "not"
    def update(self,):
        """
        updateメゾット
        """
        self.rect.centerx += self.vx
        if self.use == "on":
            self.kill()


def main():
    pg.display.set_caption("gmae")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img_2=pg.transform.flip(bg_img,True,False)
    yuka = pg.image.load("ex05/fig/renga.png")

    items = pg.sprite.Group()
    hito = Hito()
    
    tmr = 0
    x = 0
    while True:


        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if hito.type == "run":
                    hito.type = "janpup"

        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[1600-x,0])
        screen.blit(bg_img,[3200-x,0])
        screen.blit(yuka,[-x,HEIGHT/2+261])
        screen.blit(yuka,[1600-x,HEIGHT/2+261])
        screen.blit(yuka,[3200-x,HEIGHT/2+261])

        if tmr%10000 == 0:
            items.add(Item())

        for item in pg.sprite.spritecollide(hito,items,True):
            item.use = "on"
            hito.item_use(50)

        yoko,tate = check_bound(hito)
        if not yoko or not tate:
            hito.change_img("die.png",screen)
            #score.update(screen)
            gameover_str = pg.image.load("ex05/fig/gameover.png")
            screen.blit(gameover_str,[WIDTH/2-562,HEIGHT/2-141])
            pg.display.update()
            time.sleep(2)
            return

            
            

            #score.score_up(10)  # 1点アップ

        hito.update(screen)

        items.update()
        items.draw(screen)


        pg.display.update()

        tmr += 10
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
