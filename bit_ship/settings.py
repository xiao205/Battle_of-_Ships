#用于将所有设置存储在一个地方，以免代码到处添加设置
#命令行进行重新编辑png图片，进入图片所在文件夹，右键打开终端，输入mogrify *.png。
class settings:
    def __init__(self):
        #初始化游戏设置
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (230,230,230)  #背景颜色设置
       # self.ship_speed = 3 # 飞船速度
        self.ship_limit = 3 #限定飞船数量

        #子弹设置
       # self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (250,0,0)
        self.bullets_allowed = 20 #对子弹量做限定

        #外星飞船设置
       # self.alien_speed = 1.0 # 外星飞船移动速度
        self.fleet_drop_speed = 1 # 当外星飞船碰到屏幕边缘向下移动速度
        #self.fleet_direction = 1 #当值为1 是向右移动，当值为-1 是向左移动
        self.speedup_scale = 1.1 #加快游戏的倍数
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #最初对速度的设定
        self.ship_speed = 1.5  # 飞船速度
        self.bullet_speed = 3.0  #子弹速度
        self.alien_speed = 0.5  # 外星飞船移动速度
        self.alien_points = 50 #击中一个外星飞船50分


        self.fleet_direction = 1  # 当值为1 是向右移动，当值为-1 是向左移动

    def increase_speed(self):
        #提供速度设定
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale


