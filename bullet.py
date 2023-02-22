# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 00:22:07 2023

@author: tya
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船发射的子弹类"""
    
    def __init__(self,t_game):
        super().__init__()
        self.screen=t_game.screen
        self.settings=t_game.settings
        self.color=self.settings.bullet_color
        
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=t_game.ship.rect.midtop
        
        self.y=float(self.rect.y)
    
    def update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y=self.y
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        
    