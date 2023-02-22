# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:41:00 2023

@author: tya
"""

import sys
import random
import pygame
import time

from settings import Settings
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

class AlienInvasion:
    def __init__(self):
        """"初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.s_width=self.screen.get_rect().width
        self.settings.s_height=self.screen.get_rect().height
        pygame.display.set_caption("tyd game")
        
        #设置背景色
        self.bg_color=(260,260,260)
        
        #self是指向AlienInvasion自身实例的一个引用
        self.ship=Ship(self)
        
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        
        self._create_fleet()
        #飞船状态
        self.stats=GameStats(self)
        
        #创建按钮
        self.play_button = Button(self,"Begin")
        
        
    def _ship_hit(self):
        """飞船与外星人发生碰撞"""
        if self.stats.ship_left >= 0:
            self.stats.ship_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            
            
            self._create_fleet()
            self.ship.center_ship()
            
            #暂停
            time.sleep(1)
        else:
            self.stats.game_active=False
    
    def _create_fleet(self):
        """创建外星人群"""
        alien=Alien(self)
        
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.s_width-(2*alien_width)
        number_aliens_x=available_space_x//(2*alien_width)
        
        #多少行
        ship_height=self.ship.rect.height
        available_space_y = (self.settings.s_height-
                             (3*alien_height)-ship_height)
        number_rows = available_space_y//(2*alien_height)
        
        
        for row_number in range(number_rows):
            #c=random.randint(0, 8)
            #number_aliens_x -= c
            for alien_number in range(number_aliens_x):
               self._create_alien(alien_number,row_number)
        
    def _create_alien(self,alien_number,row_number):
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        a = 2*random.randint(0, 1)
        alien.x=alien_width + a*alien_width*alien_number
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height + a*alien.rect.height*row_number
        self.aliens.add(alien)
        
        
    def _check_fleet_edges(self):
        """当有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.direction *= -1
            
        
    def run_game(self):
        """begin the game  main loop"""
        while True:
            #监控键盘和鼠标事件
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            #update the screeen
            self._update_screen()
            
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #外星人和飞船碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hitted!!!")
            self._ship_hit()
            
        self._check_aliens_bottom()
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self,mouse_pos):
        """在玩家单机play按钮时开始游戏"""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and  not self.stats.game_active:
            #重置游戏设置
            self.settings.increase_speed()
            self.stats.game_active = True
            # reset game
            self.aliens.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.ship.center_ship()
        
        
    def _check_keydown_events(self,event):
        if event.key==pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key==pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()
        elif event.key==pygame.K_ESCAPE:
            sys.exit()#按q键退出
    
    
    def _check_keyup_events(self,event):
        """检查键盘"""
        if event.key == pygame.K_RIGHT:
            self.ship.move_right=False
        if event.key == pygame.K_LEFT:
            self.ship.move_left=False
    
    def _update_bullets(self):
        """更新子弹位置"""
        self.bullets.update()
            # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
    
    
    def _check_bullet_alien_collision(self):
        # 检查是否子弹击中
        #如果是删除子弹和外杏仁
        collisions=pygame.sprite.groupcollide(self.bullets, self.aliens,True,True)
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
    
    def _update_screen(self):
        """更新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
    
    
    def _fire_bullet(self):
        """"创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets)<=self.settings.bullet_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    
    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底部"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #当外星人撞到屏幕底部时，像撞到飞船一样处理
                self._ship_hit()
                break
    
class Ship:
    """管理飞船类"""
    def __init__(self,t_game):
        self.screen=t_game.screen
        self.seetings=t_game.settings
        self.screen_rect=t_game.screen.get_rect()
        
        self.image=pygame.image.load("images/ship.bmp")
        self.rect=self.image.get_rect()
        
        # 将飞船放到屏幕底部中央
        self.rect.midbottom=self.screen_rect.midbottom
        
        
        
        self.x=float(self.rect.x)
        
        #移位标记
        self.move_right=False
        self.move_left=False
        
     
    def center_ship(self):
        """让飞船居于底部居中"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        
    def blitme(self):
        self.screen.blit(self.image,self.rect)
    
    def update(self):
        if self.move_right and self.rect.right<self.screen_rect.right:
            self.x += self.seetings.ship_speed
        if self.move_left and self.rect.left>0:
            self.x -= self.seetings.ship_speed
        
            
        # 更新rect对象
        self.rect.x=self.x
        
if __name__ == '__main__':
    ai=AlienInvasion()
    ai.run_game()
    