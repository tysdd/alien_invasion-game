# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 18:25:12 2023

@author: tya
"""

import pygame.font

class Button:
    def __init__(self,t_game,msg):
        """初始化按钮"""
        self.screen = t_game.screen
        
        self.screen_rect=self.screen.get_rect()
        
        self.width,self.height=200,50
        self.button_color=(0,0,255)
        self.text_color=(255,255,255)
        self.font=pygame.font.SysFont(None, 48)
        
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        
        self._prep_msg(msg)
        
    def _prep_msg(self,msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
        
    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.bilt(self.msg_image,self.msg_image_rect)
        
        
        