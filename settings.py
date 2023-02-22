# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:58:58 2023

@author: tya
"""

class Settings:
    
    def __init__(self):
        """初始化游戏设置"""
        self.s_width=1200
        self.s_height=800
        self.bg_color=(230,230,230)
        # 飞船设置
        self.ship_speed=1.5
        #飞船数量限制
        self.ship_limit=3
        #子弹设置
        self.bullet_speed=1.0
        self.bullet_width=5
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.bullet_allowed=15
        
        # 外星人移动速度
        self.alien_speed=1.0
        #撞到边缘时向下移动速度
        self.fleet_drop_speed=10
        
        self.direction=1#1向右移
        
        #加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
        
    def initialize_dynamic_settings(self):
            self.ship_speed = 2
            self.bullet_speed=3
            self.alien_speed=1.5
            
            self.direction=1
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        
    
        