# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import json
import tools

class choice:

    def __init__(self):
        self.choiceList = []
        pass

    def add(self, dic):
        self.choiceList.append(dic)
