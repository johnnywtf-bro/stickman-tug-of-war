import pygame

BLACK = (0, 0, 0)

class Stickman:
    def __init__(self, name, height, stickman_width=20, stickman_height=60):
        self.name = name
        self.stickman_width = stickman_width
        self.stickman_height = stickman_height
        self.ground_y = height - 100
        self.head_radius = 10 

    def draw_stickman(self, x, y, screen):
        # 身體各部位座標計算
        body_top_y = y + self.head_radius
        body_bottom_y = y + self.stickman_height
        
        # 頭
        pygame.draw.circle(screen, BLACK, (x, y), self.head_radius, 2) 
        
        # 身體
        pygame.draw.line(screen, BLACK, (x, body_top_y), (x, body_bottom_y), 5) 
        
        # 手
        arm_y = body_top_y + 10 
        pygame.draw.line(screen, BLACK, (x, arm_y), (x - 15, arm_y + 20), 3)  # 左手
        pygame.draw.line(screen, BLACK, (x, arm_y), (x + 15, arm_y + 20), 3)  # 右手

        # 腳
        pygame.draw.line(screen, BLACK, (x, body_bottom_y), (x - 10, body_bottom_y + 20), 3)  # 左腳
        pygame.draw.line(screen, BLACK, (x, body_bottom_y), (x + 10, body_bottom_y + 20), 3)  # 右腳