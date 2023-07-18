import random
import shelve
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
        #screen.blit(self.img, [WIDTH/2,HEIGHT/2])


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

class Coin(pg.sprite.Sprite):
    """
    coinに関するクラス
    """
    imgs = [pg.image.load(f"ex05/fig/coin{i}.png") for i in range(1, 4)]
    def __init__(self,num):
        """

        """
        super().__init__()
        self.image = __class__.imgs[num]
        #self.image = random.choice(__class__.imgs)
        #self.image=pg.image.load("ex05/fig/coin1.png")
        self.image=pg.transform.rotozoom(self.image,0,0.1)
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH
        self.rect.centery=random.randint(HEIGHT/3,HEIGHT*2/3)
        self.vx = -10

    def update(self):
        self.rect.centerx+=self.vx


class Coin(pg.sprite.Sprite):
    """
    coinに関するクラス
    """
    imgs = [pg.image.load(f"ex05/fig/coin{i}.png") for i in range(1, 4)]
    def __init__(self):
        """

        """
        super().__init__()
        self.image = random.choice(__class__.imgs)
        #self.image=pg.image.load("ex05/fig/coin1.png")
        self.image=pg.transform.rotozoom(self.image,0,0.1)
        self.rect=self.image.get_rect()
        self.rect.centerx=WIDTH
        self.rect.centery=random.randint(HEIGHT/3,HEIGHT*2/3)
        self.vx = -10

    def update(self):
        self.rect.centerx+=self.vx


def main():
    pg.display.set_caption("gmae")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    bg_img_2=pg.transform.flip(bg_img,True,False)
    yuka = pg.image.load("ex05/fig/renga.png")

    items = pg.sprite.Group()
    hito = Hito()
    coins1 = pg.sprite.Group()
    coins2 = pg.sprite.Group()
    coins3 = pg.sprite.Group()
    score = Score()
    coins=pg.sprite.Group()

    tmr = 0
    x = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if hito.type == "run":
                    hito.type = "janpup"
        
        #for i, coin in enumerate(coins):
            #if coin.rect.colliderect(hito.rect):
                #coins[i] = None
                #print("b")
                #pg.display.update()


        x = tmr%3200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img_2,[1600-x,0])
        screen.blit(bg_img,[3200-x,0])
        screen.blit(yuka,[-x,HEIGHT/2+261])
        screen.blit(yuka,[1600-x,HEIGHT/2+261])
        screen.blit(yuka,[3200-x,HEIGHT/2+261])
        #score.score=10*len(pg.sprite.spritecollide(hito,coins,True))
        for i in pg.sprite.spritecollide(hito,coins1,True): #コインとぶつかったらスコアを1増やす
            score.score_up(10)
        for i in pg.sprite.spritecollide(hito,coins2,True): #コインとぶつかったらスコアを1増やす
            score.score_up(100)
        for i in pg.sprite.spritecollide(hito,coins3,True): #コインとぶつかったらスコアを1増やす
            score.score_up(1000)
        score.update(screen)

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
          
        hito.update(screen)

        items.update()
        items.draw(screen)
        if tmr%random.randint(1,1500)==0:
            num=random.randint(0,3)
            if num==0:
                coins1.add(Coin(num))
            elif num==1:
                coins2.add(Coin(num))
            elif num==2:
                coins3.add(Coin(num))
        print(coins1)
        print(coins2)
        print(coins3)

        coins1.update()
        coins1.draw(screen)
        coins2.update()
        coins2.draw(screen)
        coins3.update()
        coins3.draw(screen)
        
            coins.add(Coin())
            print(coins)

        coins.update()
        coins.draw(screen)

        pg.display.update()

        tmr += 10
        clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
