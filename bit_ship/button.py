#当按下开始按钮，游戏才开始
import pygame.font


class Button:
    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        #设置按钮的尺寸
        self.width = 200
        self.height = 50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)  #文本为白色
        self.font = pygame.font.SysFont(None,48)  #默认字体，大小48
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        #按钮的标签
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        #将上面的按钮属性渲染为图片
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def draw_button(self):
        #绘制一个用颜色填充的按钮
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
