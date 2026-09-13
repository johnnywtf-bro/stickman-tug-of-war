import pygame
import random

class Card:
    def __init__(self, card_type, name, description, owner):
        self.type = card_type  # buff or debuff
        self.name = name
        self.description = description
        self.owner = owner  # player or computer
        self.effect_type = "" # money, pull, push, paralyze, clean

class CardSystem:
    def __init__(self, screen, W, H):
        self.screen = screen
        self.W = W
        self.H = H
        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 50)
        
        self.player_cards = []
        self.computer_cards = []
        self.active_effects = []
        
        # 狀態
        self.player_paralyzed = False
        self.computer_paralyzed = False
        self.player_money_multiplier = 1.0
        self.computer_money_multiplier = 1.0
        self.player_tilt = 0
        self.computer_tilt = 0
        
    def draw_card(self, owner):
        rand_num = random.randint(1, 100)
        
        if rand_num < 20:  # 1-19: 金幣*2
            card_type = "buff"
            name = "money*2"
            desc = "Level Money x2"
            effect = "money"
        elif rand_num < 35:  # 20-34: 傾斜
            card_type = "buff"
            name = "pull"
            desc = "Level Pull +1"
            effect = "pull"
        elif rand_num < 50:  # 35-49: 麻痺
            card_type = "buff"
            name = "paralyze"
            desc = "Level Paralyze Enemy"
            effect = "paralyze"
        elif rand_num < 60:  # 50-59: 清除
            card_type = "buff"
            name = "clean"
            desc = "Clean All Debuffs"
            effect = "clean"
        elif rand_num < 75:  # 60-74: 金幣/2
            card_type = "debuff"
            name = "money/2"
            desc = "5 Levels Money /2"
            effect = "money"
        elif rand_num < 90:  # 75-89: 傾斜
            card_type = "debuff"
            name = "push"
            desc = "5 Levels Push +1"
            effect = "push"
        else:  # 90-100: 被麻痺
            card_type = "debuff"
            name = "paralyze you"
            desc = "5 Levels Paralyzed"
            effect = "paralyze"
        
        card = Card(card_type, name, desc, owner)
        card.effect_type = effect
        
        if owner == "player" and card_type == "debuff":
            print(f"{owner} 抽到了 Debuff: {name} used immediately")
            return card
            
        if owner == "player":
            self.player_cards.append(card)
        else:
            self.computer_cards.append(card)
        
        print(f"{owner} 抽到了: {name}")
        return card
    
    def show_draw(self, card):
        clock = pygame.time.Clock()
        for i in range(45):  
            self.screen.fill((50, 50, 50))
            
            title_text = "Draw Card!"
            title = self.title_font.render(title_text, True, "white")
            self.screen.blit(title, (self.W//2 - 100, 100))
            
            card_rect = pygame.Rect(self.W//2 - 150, 200, 300, 200)
            card_color = (100, 200, 100) if card.type == "buff" else (200, 100, 100)
            pygame.draw.rect(self.screen, card_color, card_rect, border_radius=15)
            pygame.draw.rect(self.screen, "white", card_rect, 3, border_radius=15)
            
            name_text = self.font.render(card.name, True, "white")
            desc_text = self.small_font.render(card.description, True, "white")
            type_text = self.small_font.render(f"[{card.type.upper()}]", True, "yellow")
            
            self.screen.blit(type_text, (self.W//2 - 50, 220))
            self.screen.blit(name_text, (self.W//2 - 80, 260))
            self.screen.blit(desc_text, (self.W//2 - 100, 320))
            
            pygame.display.flip()
            clock.tick(30)
    
    def draw_player_cards(self, mouse_pos, y_position):
        #玩家手牌
        buttons = []
        title = self.small_font.render("Your Cards (Click to use):", True, "black")
        self.screen.blit(title, (320, y_position - 25))
        
        x_start = 320
        y = y_position
        
        for i, card in enumerate(self.player_cards):
            rect = pygame.Rect(x_start + i * 90, y, 80, 100)
            color = (100, 200, 100) # 綠色(buff)
            
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (255, 255, 0), rect.inflate(4, 4), border_radius=8)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, "white", rect, 2, border_radius=8)
            
            # 卡牌名稱
            name_lines = [card.name] if len(card.name) <= 8 else [card.name[:len(card.name)//2], card.name[len(card.name)//2:]]
            for j, line in enumerate(name_lines):
                text = self.small_font.render(line, True, "white")
                self.screen.blit(text, text.get_rect(center=(rect.centerx, rect.centery - 10 + j * 20)))
            
            buttons.append((rect, card))
        return buttons
    
    def use_card(self, card):
        #用卡片效果
        duration = 5 if card.type == "debuff" else 1
        
        # 清除卡
        if card.effect_type == "clean":
            new_effects = []
            for effect in self.active_effects:
                if effect["card"].type == "buff":
                    new_effects.append(effect)
            self.active_effects = new_effects
            print("移除所有 Debuff")
        else:
            # 效果加入列表
            self.active_effects.append({"card": card, "level_duration": duration})
        
        # 從手牌移除
        if card in self.player_cards:
            self.player_cards.remove(card)
        
        # 更新狀態
        self.sync_effects()
        
    def next_level(self):
        #過關 更新效果用
        active_list = []
        for effect in self.active_effects:
            effect["level_duration"] -= 1
            # 剩餘 Level
            if effect["level_duration"] > 0:
                active_list.append(effect)
            else:
                print(f"effect end: {effect['card'].name}")
                
        self.active_effects = active_list
        # 更新狀態
        self.sync_effects()
        
    def sync_effects(self):
        #更新狀態
        # 重置所有數值
        self.player_paralyzed = False
        self.computer_paralyzed = False
        self.player_money_multiplier = 1.0
        self.computer_money_multiplier = 1.0
        self.player_tilt = 0
        self.computer_tilt = 0
        
        for item in self.active_effects:
            card = item["card"]
            owner = card.owner
            
            if card.effect_type == "paralyze":
                # Buff:電腦麻痺,Debuff:玩家麻痺
                if card.type == "buff":
                     if owner == "player": self.computer_paralyzed = True
                     else: self.player_paralyzed = True
                else: # debuff
                     if owner == "player": self.player_paralyzed = True
                     else: self.computer_paralyzed = True

            elif card.effect_type == "money":
                if card.type == "buff":
                    if owner == "player": self.player_money_multiplier *= 2.0
                    else: self.computer_money_multiplier *= 2.0
                else: # debuff
                    if owner == "player": self.player_money_multiplier *= 0.5
                    else: self.computer_money_multiplier *= 0.5

            elif card.effect_type == "pull":
                if owner == "player": self.player_tilt += 1
                else: self.computer_tilt += 1
                
            elif card.effect_type == "push":
                if owner == "player": self.player_tilt -= 1
                else: self.computer_tilt -= 1

    def draw_active_effects(self, y_position):
        y_offset = y_position
        
        # 顯示效果
        for i, item in enumerate(self.active_effects):
            card = item["card"]
            duration = item["level_duration"]
            color = (100, 255, 100) if card.type == "buff" else (255, 100, 100)
            
            text = f"{card.name}: {duration} Level left"
            rendered = self.small_font.render(text, True, color)
            
            x_pos = 320 if card.owner == "player" else self.W - 220
            self.screen.blit(rendered, (x_pos, y_offset + i * 20))

    def get_coin_multiplier(self, owner):
        return self.player_money_multiplier if owner == "player" else self.computer_money_multiplier
    
    def get_tilt_power(self, owner):
        return self.player_tilt if owner == "player" else self.computer_tilt
        