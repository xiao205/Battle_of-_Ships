#外星飞船
import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self,ai_game):
        #初始化外星飞船
        super().__init__()
        self.screen = ai_game.screen # 获取屏幕
        self.image = pygame.image.load("image/alien.png") #加载图片
        self.rect = self.image.get_rect() # 获取图片的位置
        self.settings = ai_game.settings  #调用主程序中的settings
        #每个外星飞船最初在屏幕的左上角附件设定距左边距的宽和距上边距的高
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    def check_edges(self):
        # 检查外星飞船位于屏幕边缘返回Ture
        screen_rect = self.screen.get_rect() #获得屏幕坐标
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # 外星飞船向右移动
        # 乘于self.settings.fleet_direction 来分左右移动
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x



