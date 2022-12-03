"""外星飞船碰撞飞船时，需要执行跟多任务，
1 删除剩余的外星飞船与子弹
2 让飞船重新居中
3 创建一批新的外星飞船
"""
class GameStats:
    #用于记录飞船被碰撞次数
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats() #用于初始化大部分统计信息
        self.game_active = False # 游戏运行的标志
        self.high_score = 0 # 初始最高分数
    def reset_stats(self):
        #初始化在游戏期间可能变化的统计信息
        self.ship_left = self.settings.ship_limit  # 统计飞船数量
        self.score = 0 #用于计分
        self.level = 1 #设置最初玩家等级

