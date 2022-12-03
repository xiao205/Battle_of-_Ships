import pygame
import sys
from time import sleep    #以便飞船在碰撞可以让游戏暂停几秒
from settings import settings  # 导入设置
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
class AlienInvasion:
    # 屏幕显示
    def __init__(self):
        pygame.init() #来初始化背景设置
        #创建一个窗口
        self.settings = settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)    #设置全屏幕
        self.settings.screen_width = self.screen.get_rect().width #获取屏幕宽度
        self.settings.screen_height = self.screen.get_rect().height  #获取屏幕高度
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)  # 加载飞船
        self.bullets = pygame.sprite.Group() #一组编组用于存储子弹
        self.aliens = pygame.sprite.Group() #一组编组存储与外星飞船
        self._create_fleet()
        #设置背景颜色
        self.bg_color = (self.settings.bg_color)
        self.stats = GameStats(self) #实例化一个统计信息的实例
        self.play_button = Button(self,"play")  #实例化按钮，并传入文字
        self.sb = Scoreboard(self)  # 实例化积分类

    #外星飞船相关
    def _create_alien(self,alien_number,row_number):
        #创建一个外星飞船
        # 创建一行外星飞船
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number  # 获取x坐标
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number #获取y坐标
        self.aliens.add(alien)  # 加入到编组
    def _create_fleet(self):
        #创建外星飞船，添加到编组中
        alien = Alien(self)
        #创建一行外星飞船
        alien_width = alien.rect.width
        # 获取屏幕可用宽度 之间的空白距离减去2个外星飞船的宽度
        available_space_x = self.settings.screen_width - (2 * alien_width)
        #一行外星飞船数量，取整
        alien_height = alien.rect.height   # 外星飞船高度
        ship_height = self.ship.rect.height
        #获取屏幕可用高度， 减去之间的空白距离和外星飞船高度，飞船高度
        available_space_y = self.settings.screen_height - (2 * alien_height) - ship_height
        # 可以放几行外星飞船
        number_rows = available_space_y // (3 * alien_height)
        # 一行可以放外星飞船的个数
        number_aliens_x = available_space_x // (2 * alien_width)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)
    def _check_fleet_edges(self):
        #外星飞船处于屏幕边缘采取的措施
        for alien in self.aliens.sprites(): # 循环编组中的外星飞船
            if alien.check_edges():  # 调用该函数返回True表示处于边缘
                self._change_fleet_direction()
    def _check_aliens_bottom(self):
        #当外星飞船到达屏幕底端
        screen_rect= self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()  # 当外星飞船到达底部，与飞船碰撞进行一样操作
                break # 结束循环
    def _change_fleet_direction(self):
        #将外星飞创下移
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _ship_hit(self):
        #飞船被撞
        if self.stats.ship_left > 0:
            #self.ship.image = pygame.image.load("image/ship2.png")
            self.stats.ship_left -= 1 # 剩余飞船减一
            self.sb.prep_ships()  #减1后调用显示
            #清空剩余的外星飞船与子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人并将飞船放在中央位置
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False  #当限定的飞船小于0，标志设为false
            #在游戏结束后让鼠标显示
            pygame.mouse.set_visible(True)
    def _update_aliens(self):
        #更新外星飞船的位置
        self._check_fleet_edges()
        self.aliens.update() #对外星飞船编组调用update方法
        #检测外星飞船与飞船碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #检查外星飞船到达底部
        self._check_aliens_bottom()


    #子弹相关
    def _fire_bullet(self):
        #创建一颗子弹，加入到组中
        if len(self.bullets) < self.settings.bullets_allowed:
            #当存储的子弹小于允许的子弹量
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) #加入到编组
    def _update_bullets(self):
        #更新子弹位置并删除消失的子弹
        self.bullets.update() #更新子弹位置
        # 因为不能从for循环遍历的列表或编组中删除元素，所以必须遍历编组的副本，
        for bullet in self.bullets.copy():  #
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))  # 打印当前右多少颗子弹存储
        self._check_bullet_alien_conllisions()
    def _check_bullet_alien_conllisions(self):
        #检查子弹击中外星飞船
        #如果是删除子弹与外星飞船
        #这个方法会获取重合的子弹与外星飞船返回一个字典，True会将子弹与外星飞船消失
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
        if not self.aliens:
            #新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed() #当新的一批时设定新速度，来加快游戏

            #提升玩家等级
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)# 分数增加
            self.sb.prep_score()
            self.sb.check_high_socre()

    #按键相关设置
    def _check_play_button(self,mouse_pos):
        #检查是否点击play按钮，mouse_pos是传入的鼠标点击坐标
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True
            self.stats.score = 0  #按键后初始化分数
            self.sb.prep_score() # 将分数重置
            self.sb.prep_level()
            self.sb.prep_ships()    #显示飞船数量
            # 点击开始进行游戏重置
            self.aliens.empty()
            self.bullets.empty()
            #创建一群新的外星飞船和飞船
            self._create_fleet()
            self.ship.center_ship() # 创建飞船
            #在游戏开始后将鼠标隐藏起来
            pygame.mouse.set_visible(False)
            # 设定速度为初始状态
            self.settings.initialize_dynamic_settings()

    #按键事件相关
    def _check_keydown_event(self,event):
        #按下左右键设置
        if event.key == pygame.K_RIGHT:  # 事件类型为右箭头
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:  #按q键退出
            sys.exit()
    def _check_keyup_event(self,event):
        #松开后
        if event.key == pygame.K_RIGHT:  # 事件类型为右箭头
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    def _check_events(self):
        # 将管理类事件代码放在这个函数中
        # 监听键盘和鼠标
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:  #事件类型为按键
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:  # 事件类型为按键
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN: # 获取鼠标点击的事件
                mouse_pos = pygame.mouse.get_pos()  # 鼠标点击坐标返回一个元组
                self._check_play_button(mouse_pos)


    def _update_screen(self):
        #将屏幕更新代码放在函数中
        # 每次循环都回值屏幕
        self.screen.fill(self.bg_color)  # 将夜色填充屏幕
        self.ship.blitme()  # 在屏幕上绘制飞船
        #在屏幕显示子弹
        for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        # 让屏幕可见
        self.aliens.draw(self.screen) #让外星人在屏幕现身
        self.sb.show_score()  # 在屏幕可见
        # 让按钮在屏幕可见
        if not self.stats.game_active:  # 如果不为true 就显示按钮
            self.play_button.draw_button()
        pygame.display.flip()  # 将不断更新屏幕


   #主程序
    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()