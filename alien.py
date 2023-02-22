# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 12:32:35 2023

@author: tya
"""
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,t_game):
        super().__init__()
        self.screen=t_game.screen
        self.settings=t_game.settings
        #加载图片
        self.image=pygame.image.load("images/alien.bmp")
        self.rect=self.image.get_rect()
        # 最初出现在屏幕左上角
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        
        self.x=float(self.rect.x)
        
        
    def update(self):
        """向左右移动外星人"""
        self.x += (self.settings.alien_speed*self.settings.direction)
        self.rect.x = self.x
            
    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True