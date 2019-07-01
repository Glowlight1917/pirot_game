# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import json
import spriteMod

import tools

class sequence:
    """
    シーケンス処理用のクラス
    """

    def __init__(self, window, data):
        self.data = data
        self.window = window
        self.spriteGroup = pygame.sprite.RenderUpdates()
        self.nextSequence = []
        self.back_pic = None

    def load_pic(image_file_path):
        """
        パスから画像を読み込む関数

        Parameters
        ----------
        image_file_path: str
            画像のパス

        Returns
        -------
        pygameで扱う画像データ
        """

        return pygame.image.load(image_file_path).convert_alpha()

    def split_pic(image_file, tip_size_x, tip_size_y):
        """
        チップ画像を分割して読み込む

        Parameters
        ----------
        image_file: str
            画像のパス

        tip_size_x: int
            最小単位の幅

        tip_size_y: int
            最小単位の高さ

        Returns
        -------
        tip_list: list
            分割した画像データを含んだリスト
            左上から右下にかけてidを振っている
        """

        image = self.load_pic(image_file)
        image_size = image.get_size()
        tip_index = (image_size[0] // tip_size_x, image_size[1] // tip_size_y)
        tip_list = []

        for j in range(0, tip_index[1]): #vertical
            for i in range(0, tip_index[0]): #horizontal
                surface = pygame.Surface((tip_size_x, tip_size_y), SRCALPHA)
                x = tip_size_x * i
                y = tip_size_y * j
                surface.blit(image, (0, 0), (x, y, x + tip_size_x, y + tip_size_y))
                tip_list.append(surface)

        return tip_list

    def setBackPic(self, pic):
        """
        背景画像を設定する

        Parameters
        ----------
        pic: str
            読み込む画像のパス
        """

        self.back_pic = tools.load_pic(pic)

    def update(self):
        pass

    def keys(self, key):
        pass

    def draw(self, screen):
        if self.back_pic != None:
            screen.blit(self.back_pic, self.back_pic.get_rect())

class titlesec(sequence):
    '''
    map_array: マップ配列データ
    maptip: マップチップリスト
    tipsize: マップチップの大きさ
    layer: レイヤー. マップ配列を格納したリスト
    scroll: スクロール量
    stage_size: ステージの大きさ
    '''

    def __init__(self, window, data):
        super().__init__(window, data)
        
        self.cnt = 0
        self.select = []
        self.now = 0

        #次のシーケンスを登録
        seq = stage(window, self.data)
        seq.setBackPic('bgp.png')
        self.nextSequence.append(seq)
        self.setBackPic('title.png')

        self.select.append('start')
        self.select.append('end')

    def update(self):
        pass

    def keys(self, keyevents):
        num = len(self.select)
        key = keyevents[0]

        if len(keyevents) == 1:
            return

        if keyevents[1].key == K_UP:
            self.now = (self.now - 1) % num

        if keyevents[1].key == K_DOWN:
            self.now = (self.now + 1) % num

        if keyevents[1].key == K_RETURN:
            if self.select[self.now] == 'start':
                self.window.moveSequence(self.nextSequence[0])

            if self.select[self.now] == 'end':
                pygame.quit()
                sys.exit()

    def draw(self, screen):
        super().draw(screen)

        f = lambda x: ' #' if x == self.now else ' '
        font2 = pygame.font.SysFont(None, 50)
        text1 = font2.render(self.select[0] + f(0), True, (255,0,0))
        text2 = font2.render(self.select[1] + f(1), True, (255,0,0))
        screen.blit(text1, (260,300))
        screen.blit(text2, (260,340))

class pause(sequence):
    '''
    map_array: マップ配列データ
    maptip: マップチップリスト
    tipsize: マップチップの大きさ
    layer: レイヤー. マップ配列を格納したリスト
    scroll: スクロール量
    stage_size: ステージの大きさ
    '''

    def __init__(self, window, data):
        super().__init__(window, data)

        self.cnt = 0
        self.select = []
        self.now = 0

        self.image = tools.load_pic('pause.png')
        self.select.append('start')
        self.select.append('aaaaa')
        self.select.append('bbbbb')

    def update(self):
        pass

    def keys(self, keyevents):
        num = len(self.select)
        key = keyevents[0]

        if len(keyevents) == 1:
            return

        if keyevents[1].key == K_UP:
           self.now = (self.now - 1) % num
        if keyevents[1].key == K_DOWN:
            self.now = (self.now + 1) % num
        if keyevents[1].key == K_SPACE:
            self.window.moveSequence(self.nextSequence[0])

        '''
        if key[K_UP]:
            self.now = (self.now - 1) % num

        if key[K_DOWN]:
            self.now = (self.now + 1) % num

        if key[K_SPACE]:
            if self.select[self.now] == 'start':
                self.window.moveSequence(self.nextSequence[0])

            if self.select[self.now] == 'Pause Test':
                pass
        '''

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.image, (64, 60)) 

class stage(sequence):
    '''
    map_array: マップ配列データ
    maptip: マップチップリスト
    tipsize: マップチップの大きさ
    layer: レイヤー. マップ配列を格納したリスト
    scroll: スクロール量
    stage_size: ステージの大きさ
    '''

    def __init__(self, window, data):
        super().__init__(window, data)

        self.scroll_x = 0
        self.scroll_y = 0
        self.tipsize = (32,32)
        self.map_array = None

        self.player = spriteMod.spriteClass(self)
        self.spriteGroup.add(self.player)
        self.load_map_array('map2.txt')
        self.load_tip('map.png',(32,32))
        self.setBackPic('bgp.png')

        self.status = tools.load_pic('status.png')

        #ポーズ画面用のシーケンス
        print(self.nextSequence)
        pauseSeq = pause(window, data)
        self.nextSequence.append(pauseSeq)
        pauseSeq.nextSequence.append(self)

    #マップ配列を読み込む
    def load_map_array(self, path):
        map_array = []

        with open(path, 'r') as fp:
            mapdata = fp.read().split('\n')

        for line in mapdata:
            #空白行を無視
            if line == '': continue

            map_array.append(list(map(lambda x: int(x), line.split(','))))

        self.map_array = map_array

    def getTip(self, x, y):
        X = int(x)
        Y = int(y)

        if X < 0 or X >= len(self.map_array[0]):
            return [0,0,0]

        if Y < 0 or Y >= len(self.map_array):
            return [0,0,0]

        return [int(x), int(y), self.map_array[int(y)][int(x)]]

    def getMapTip(self, sp):
        tiplist = []
        mx = self.tipsize[0]
        my = self.tipsize[1]

        tiplist.append(self.getTip(sp.x // mx, sp.y // my))
        tiplist.append(self.getTip((sp.x + sp.size[0]) // mx, (sp.y) // my))
        tiplist.append(self.getTip((sp.x) // mx, (sp.y + sp.size[1]) // my))
        tiplist.append(self.getTip((sp.x + sp.size[0]) // mx, (sp.y + sp.size[1]) // my))

        return tiplist

    def getNextMapTip(self, sp, st):
        tiplist = []
        mx = self.tipsize[0]
        my = self.tipsize[1]

        if st == 'x':
            vx = sp.vx
            vy = 0
        else:
            vx = 0
            vy = sp.vy

        tiplist.append(self.getTip((sp.x + vx) // mx, (sp.y + vy) // my))
        tiplist.append(self.getTip((sp.x + vx + sp.size[0]-1) // mx, (sp.y + vy) // my))
        tiplist.append(self.getTip((sp.x + vx) // mx, (sp.y + vy + sp.size[1]-1) // my))
        tiplist.append(self.getTip((sp.x + vx + sp.size[0]-1) // mx, (sp.y + vy + sp.size[1]-1) // my))

        return tiplist

    def getStageSize(self):
        return (self.tipsize[0]*len(self.map_array[0]),
                self.tipsize[1]*len(self.map_array))

    #スクロール処理をする. x,yは主人公の座標
    def scroll(self, x, y):
        screen_size = self.data["screen"]["size"]
        width = screen_size[0]
        height = screen_size[1]

        #主人公が画面の中央に見えるようにする
        self.scroll_x = x - width/2
        self.scroll_y = y - height/2

        mapsizey = len(self.map_array)
        mapsizex = len(self.map_array[0])

        #境界条件 
        if self.scroll_x < 0: self.scroll_x = 0
        if self.scroll_y < 0: self.scroll_y = 0
        if self.scroll_x > self.tipsize[0]*mapsizex - width: self.scroll_x = self.tipsize[0]*mapsizex - width
        if self.scroll_y > self.tipsize[1]*mapsizey - height: self.scroll_y = self.tipsize[1]*mapsizey - height
       
    #スプライトの操作
    def keys(self, keyevents):
        key = keyevents[0]

        if key[K_RIGHT]:
           self.player.vx = 4 
           self.player.flipImage("right")
        if key[K_LEFT]:
           self.player.vx = -4 
           self.player.flipImage("left")
        if key[K_j]:
           if self.player.g > 0:
               self.player.vy = -12 
           else:
               self.player.vy = 12

        if len(keyevents) == 1:
            return

        #ポーズ処理
        if keyevents[1].key == K_SPACE:
            self.window.moveSequence(self.nextSequence[0])
        if keyevents[1].key == K_k:
           self.spriteGroup.add(self.player.attack())

    #マップチップ画像を分割
    def load_tip(self, tipfile, tipsize):
        self.tip_size = tipsize 
        self.tip_list = tools.split_pic(tipfile, tipsize[0], tipsize[1])

    def update(self):
        self.spriteGroup.update()
        self.scroll(self.player.x, self.player.y)

    #ステージを描画
    def draw(self, screen):
        super().draw(screen)

        #NOTE: 描画する配列の範囲を制限する. 画面に映る部分だけ描画
        for ny, line in enumerate(self.map_array):
            for nx, tip in enumerate(line):
                if self.tip_list[int(tip)] == 0:
                    continue

                #マップスクロールの量だけ引く
                screen.blit(self.tip_list[int(tip)], 
                            (self.tip_size[0] * nx - self.scroll_x,
                             self.tip_size[1] * ny - self.scroll_y))

        #スプライトの描画
        self.spriteGroup.draw(screen)

        screen.blit(self.status, (0, 0))
        font = pygame.font.SysFont(None, 20)
        hp = font.render(self.player.hp * '#', True, (0,0,255))
        remain = font.render(str(self.player.remain), True, (0,0,255))
        screen.blit(hp, (30,10))
        screen.blit(remain, (160,10))
