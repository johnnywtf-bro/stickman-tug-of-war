import pygame
import sys

class MainMenu:
    def __init__(self, screen, W, H):
        self.screen = screen
        self.W = W
        self.H = H
        self.font = pygame.font.Font(None, 50) 
        self.small_font = pygame.font.Font(None, 30)
        self.difficulty = "normal"  # 預設難度
        
    def main_menu(self):
        # 主選單
        while True:
            self.screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()
            
            # 標題
            title = self.font.render("Tug of War", True, "black")
            self.screen.blit(title, (self.W//2 - 150, 200))

            # 主按鈕
            start_button = self.draw_button("START", self.W//2 - 100, 300, 200, 80, (0, 180, 0), (0, 230, 0), mouse_pos)
            leave_button = self.draw_button("LEAVE", self.W//2 - 100, 420, 200, 80, (180, 0, 0), (230, 0, 0), mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(mouse_pos):
                        # 點START後進入難度選擇
                        selected_difficulty = self.difficulty_select()
                        if selected_difficulty:
                            return ("START", selected_difficulty) # return
                    elif leave_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    
            pygame.display.flip()
    
    def difficulty_select(self):
        #難度選擇
        while True:
            self.screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()
            
            # 標題
            title = self.font.render("difficulty", True, "black")
            self.screen.blit(title, (self.W//2 - 100, 150))

            # 按鈕
            easy_button = self.draw_button("easy", self.W//2 - 100, 250, 200, 80, 
                                          (100, 200, 100), (150, 250, 150), mouse_pos)
            normal_button = self.draw_button("normal", self.W//2 - 100, 360, 200, 80, 
                                            (200, 200, 100), (250, 250, 150), mouse_pos)
            hard_button = self.draw_button("hard", self.W//2 - 100, 470, 200, 80, 
                                          (200, 100, 100), (250, 150, 150), mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(mouse_pos):
                        return "easy"
                    elif normal_button.collidepoint(mouse_pos):
                        return "normal"
                    elif hard_button.collidepoint(mouse_pos):
                        return "hard"
                    
            pygame.display.flip()
            
    def draw_button(self,text, x, y, w, h, inactive_color, active_color, mouse_pos):
        rect = pygame.Rect(x, y, w, h)
        color = active_color if rect.collidepoint(mouse_pos) else inactive_color
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        
        text_surface = self.font.render(text, True, "white")
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        return rect
    
    def draw_small_button(self, text, x, y, w, h, inactive_color, active_color, mouse_pos, selected=False):
        rect = pygame.Rect(x, y, w, h)
        color = active_color if rect.collidepoint(mouse_pos) else inactive_color
        
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        
        text_surface = self.small_font.render(text, True, "white")
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        return rect