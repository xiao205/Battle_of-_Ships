# 绘制飞船
import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_game):  #ai_game  指向AlienInvasion这个主类
        super().__init__()
        #初始化飞船并设置初始化位置
        self.screen = ai_game.screen
        self.settings = ai_game.settings  #导入设置模块后创建个属性
        self.screen_rect = ai_game.screen.get_rect()  #访问屏幕，让飞船放在屏幕上
        #加载飞船图像并获取外接矩形
        self.image = pygame.image.load('image/ship3.png')
        self.rect = self.image.get_rect()  #飞船的rect属性，用于指定飞船位置

        # 对新飞船放在屏幕底部
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        #移动标识
        self.moving_right = False
        self.moving_left = False
    def update(self):       # 飞船向右移动
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #将self.x更新到self.rect.x
        self.rect.x = self.x
    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image,self.rect)
    def center_ship(self):
        #将飞船居中
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
