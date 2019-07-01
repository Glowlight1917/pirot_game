# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import json
import tools

class spriteClass(pygame.sprite.Sprite):

    def __init__(self, sequence):
        pygame.sprite.Sprite.__init__(self)

        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.size = (24,24)
        self.tiplist = None
        self.image = None
        self.sensors = [(0,0),(24,0),(24,24),(0,24)]
        self.speedLimit = 32
        self.g = 1
        self.hp = 5
        self.remain = 5
        self.direction = (1,0)
        self.energy = 1000

        self.sequence = sequence
        self.setImage('sprites.png', self.size)
        self.rect = Rect(self.x,self.y,self.size[0],self.size[1])

    def setImage(self, tipfile, tipsize):
        self.size = tipsize 
        self.tiplist = tools.split_pic(tipfile, tipsize[0], tipsize[1])
        self.image = self.tiplist[0]

    #画像の方向転換
    def flipImage(self, n):
        if n == "right":
            self.image = self.tiplist[0]
            self.direction = (1,0)
        if n == "left":
            self.image = self.tiplist[2]
            self.direction = (-1,0)

    #いつどの方向に格子を通過するかを調べる関数
    def getCollideList(self):
        collideList = []
        tipx = self.sequence.tipsize[0]
        tipy = self.sequence.tipsize[1]
        maxnx = int(self.speedLimit / tipx)
        maxny = int(self.speedLimit / tipy)

        #スプライトのセンサーを走査
        for num, sensor in enumerate(self.sensors):
            x0 = self.x + sensor[0] - tipx*int((self.x + sensor[0])/tipx) 
            y0 = self.y + sensor[1] - tipy*int((self.y + sensor[1])/tipy)


            '''
            データ形式: (センサーid, 移動方向, 通過時刻)

            #処理を一般の速度に拡張する場合
                maxn = int(speedLimit / tipsize)
                かかる時間は
                (n*tipx - x0)/self.vx (ただし, 1 <= n <= maxn)

            '''

            for n in range(0, maxnx):
                if tipx - x0 < abs(self.vx):
                    if self.vx > 0:
                        collideList.append((num, 'right', ((n+1)*tipx - x0)/self.vx))
                    else:
                        collideList.append((num, 'left', -((n+1)*tipx - x0)/self.vx))


            for n in range(0, maxny):
                if tipy - y0 < abs(self.vy):
                    if self.vy > 0:
                        collideList.append((num, 'down', ((n+1)*tipy - y0)/self.vy))
                    else:
                        collideList.append((num, 'up', -((n+1)*tipy - y0)/self.vy))
        
        return sorted(collideList, key=lambda elm: elm[2])

    def attack(self):
        b = bullet(self.sequence)
        b.x = self.x
        b.y = self.y
        b.vx = self.vx + 10*self.direction[0]
        return b

    def update(self):
        mapsize = self.sequence.getStageSize()
        nexttipX = self.sequence.getNextMapTip(self, 'x')
        nexttipY = self.sequence.getNextMapTip(self, 'y')


        if self.vy > 12:
            self.vy = 12

        if self.vy < -12:
            self.vy = -12

        aaaa = range(11,28)

        #right
        if self.vx > 0 and (nexttipX[1][2] in aaaa or nexttipX[3][2] in aaaa):
            self.x = 32*(int(self.x + self.vx + self.size[1]-1) // 32) - self.size[0]
            self.vx = 0

        #left
        if self.vx < 0 and (nexttipX[0][2] in aaaa or nexttipX[2][2] in aaaa):
            self.x = 32*(int(self.x + self.vx) // 32) + 32
            self.vx = 0

        self.vx -= 0.125*self.vx
        self.x += self.vx

       
        self.y += self.vy
        self.vy += self.g
        #down
        if self.vy > 0 and (nexttipY[2][2] in aaaa or nexttipY[3][2] in aaaa):
            self.y = 32*(int(self.y + self.vy + self.size[1]-1) // 32) - self.size[1]
            self.vy = 0

        #up
        if self.vy < 0 and (nexttipY[0][2] in aaaa or nexttipY[1][2] in aaaa):
            self.y = 32*(int(self.y + self.vy) // 32) + 32
            self.vy = 0

        maptip = self.sequence.getMapTip(self)
        if 36 in (maptip[0][2], maptip[1][2], maptip[2][2], maptip[3][2]):
            self.g = -1

        if 37 in (maptip[0][2], maptip[1][2], maptip[2][2], maptip[3][2]):
            self.g = 1

        '''
        if self.x < 0: 
            self.x = 0
            self.vx = 0

        if self.y < 0:
            self.y = 0
            self.vy = 0

        if self.x > mapsize[0] - self.size[0]-1: 
            self.x = mapsize[0] - self.size[0]-1 
            self.vx = 0

        if self.y > mapsize[1] - self.size[1]-1: 
            self.y = mapsize[1] - self.size[1]-1 
            self.vy = 0
        '''
        if self.y > mapsize[1] -1: 
            self.remain -= 1
            self.x = 0
            self.y = 0


        scrollx = self.sequence.scroll_x
        scrolly = self.sequence.scroll_y
        self.rect = Rect(self.x - scrollx, self.y - scrolly, self.size[0], self.size[1]) 

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class bullet(spriteClass):
    def __init__(self, sequence):
        super().__init__(sequence)

        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.size = (8,8)

        self.tiplist = None
        self.image = None

        #self.speed = 10
        self.sequence = sequence
        self.setImage('bullets.png', self.size)
        self.rect = Rect(self.x,self.y,self.size[0],self.size[1])

    def setImage(self, tipfile, tipsize):
        self.size = tipsize 
        self.tiplist = tools.split_pic(tipfile, tipsize[0], tipsize[1])
        self.image = self.tiplist[1]

    #画像の方向転換
    def flipImage(self, n):
        pass

    def update(self):
        mapsize = self.sequence.getStageSize()

        self.x += self.vx
        self.y += self.vy

        if self.x > mapsize[0] - self.size[0]-1: 
            self.x = mapsize[0] - self.size[0]-1 
            self.vx = 0

        if self.y > mapsize[1] - self.size[1]-1: 
            self.y = mapsize[1] - self.size[1]-1 
            self.vy = 0

        scrollx = self.sequence.scroll_x
        scrolly = self.sequence.scroll_y
        self.rect = Rect(self.x - scrollx, self.y - scrolly, self.size[0], self.size[1]) 

    def draw(self, screen):
        screen.blit(self.image, self.rect)
