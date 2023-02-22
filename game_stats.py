# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 21:23:18 2023

@author: tya
"""

class GameStats:
    """跟踪统计游戏信息"""
    def __init__(self,t_game):
        self.settings=t_game.settings
        self.reset_stats()
        #游戏是否开启
        self.game_active=True
        
    def reset_stats(self):
        self.ship_left=self.settings.ship_limit
        