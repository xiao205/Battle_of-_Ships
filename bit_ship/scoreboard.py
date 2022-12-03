#用于分数设置
import pygame.font
from pygame.sprite import Group
from ship import Ship  #准备编写显示的飞船组
class Scoreboard:
    def __init__(self,ai_game):
        #初始化得分涉及到的属性
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        #self.score = 0  # 用于计分
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48) # s设定字体大小
        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level() # 玩家等级
        self.prep_ships() #显示飞船
    def prep_score(self):
        #将得分转为图像
        rounded_score = round(self.stats.score,-1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)

        #在屏幕右上角显示
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 # 据屏幕右边距20
        self.score_rect.top = 20  #距屏幕顶部20
    def prep_high_score(self):
        #将最高分数渲染为图片
        high_score = round(self.stats.high_score,-1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)

        #将放在顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)  #显示最高分数
        self.screen.blit(self.level_image,self.level_rect)  # 显示玩家等级
        self.ships.draw(self.screen)   #调用draw来绘制飞船

    def check_high_socre(self):
        #检查是否右最高分数产生
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        #将玩家等价渲染为图片
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # 将放在顶部中央
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        #显示剩余飞船
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)