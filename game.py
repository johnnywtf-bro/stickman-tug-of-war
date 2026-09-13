import pygame
import threading
import random
import time
from stickman import Stickman
from main_menu import MainMenu
from card import CardSystem

pygame.init()
W, H = 1000, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Tug of War")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 60)

pos = 0.0                #繩子位置
player_click_count = 0   #玩家點擊
computer_click_count = 0 #電腦點擊

use_mutex = True         #mutex開關
mutex = threading.Lock() #互斥鎖
game_over = False        #輸贏

level = 1
coins = 0
gear_power = 0
gear_power_2 = 0
gear_power_3 = 0
gear_power_4 = 0
gear_power_5 = 0
click_power = 1 

# 新增:難度和抽卡系統
difficulty = "normal"
card_system = None
computer_difficulty_multi = 1.0
tilt_timer = 0  # 傾斜效果計時器

#race condition偵測
def print_status():
    expected_pos = computer_click_count - player_click_count
    gear_total_power = gear_power + gear_power_2 + gear_power_3 + gear_power_4 + gear_power_5
    if expected_pos != pos:
        print("race Condition")
    print(f"電腦按: {int(computer_click_count)} , 玩家按: {int(player_click_count)} , (Gear: {gear_total_power}) | 應該pos: {int(expected_pos)}, 實際pos {int(pos)}")


#執行緒
# 電腦執行緒
def computer():
    global pos, computer_click_count
    while not game_over:
        wait = max(0.1, 0.5 / (1 + level * 0.5)) * (1.0 / computer_difficulty_multi)
        time.sleep(random.uniform(wait * 0.1, wait * 1))
        if not game_over:
            # 檢查是否被麻痺
            if card_system and card_system.computer_paralyzed:
                continue
            
            if use_mutex: 
                mutex.acquire()
            try:
                temp = pos
                pos = temp + 1
                computer_click_count += 1
                print_status()
            finally:
                if use_mutex: 
                    mutex.release()


# gear執行緒
def gears():
    global pos, player_click_count, coins
    while not game_over:
        time.sleep(1.0)
        if gear_power > 0 and not game_over:
            # 檢查是否被麻痺
            if card_system and card_system.player_paralyzed:
                continue
                
            if use_mutex: 
                mutex.acquire()
            try:
                temp = pos
                pos = temp - gear_power
                player_click_count += gear_power
                multiplier = card_system.get_coin_multiplier("player") if card_system else 1.0
                coins += gear_power * 0.1 * multiplier
                print_status()
            finally:
                if use_mutex: 
                    mutex.release()

def gears_2():
    global pos, player_click_count, coins
    while not game_over:
        time.sleep(1.0)
        if gear_power_2 > 0 and not game_over:
            if card_system and card_system.player_paralyzed:
                continue
            if use_mutex:
                mutex.acquire()
            try:
                temp = pos
                pos = temp - gear_power_2
                player_click_count += gear_power_2
                multiplier = card_system.get_coin_multiplier("player") if card_system else 1.0
                coins += gear_power_2 * 0.5 * multiplier
                print_status()
            finally:
                if use_mutex:
                    mutex.release()

def gears_3():
    global pos, player_click_count, coins
    while not game_over:
        time.sleep(0.8)
        if gear_power_3 > 0 and not game_over:
            if card_system and card_system.player_paralyzed:
                continue
            if use_mutex:
                mutex.acquire()
            try:
                temp = pos
                pos = temp - gear_power_3
                player_click_count += gear_power_3
                multiplier = card_system.get_coin_multiplier("player") if card_system else 1.0
                coins += gear_power_3 * 1 * multiplier
                print_status()
            finally:
                if use_mutex:
                    mutex.release()

def gears_4():
    global pos, player_click_count, coins
    while not game_over:
        time.sleep(0.5)
        if gear_power_4 > 0 and not game_over:
            if card_system and card_system.player_paralyzed:
                continue
            if use_mutex:
                mutex.acquire()
            try:
                temp = pos
                pos = temp - gear_power_4
                player_click_count += gear_power_4
                multiplier = card_system.get_coin_multiplier("player") if card_system else 1.0
                coins += gear_power_4 * 2 * multiplier
                print_status()
            finally:
                if use_mutex:
                    mutex.release()

def gears_5():
    global pos, player_click_count, coins
    while not game_over:
        time.sleep(0.2)
        if gear_power_5 > 0 and not game_over:
            if card_system and card_system.player_paralyzed:
                continue
            if use_mutex:
                mutex.acquire()
            try:
                temp = pos
                pos = temp - gear_power_5
                player_click_count += gear_power_5
                multiplier = card_system.get_coin_multiplier("player") if card_system else 1.0
                coins += gear_power_5 * 3 * multiplier
                print_status()
            finally:
                if use_mutex:
                    mutex.release()

# 傾斜執行緒
def tilt_power():
    global pos, player_click_count, computer_click_count
    while not game_over:
        time.sleep(0.5)
        if not game_over and card_system:
            player_tilt = card_system.get_tilt_power("player")
            computer_tilt = card_system.get_tilt_power("computer")
            
            total_tilt = player_tilt - computer_tilt  #玩家可以任意時間使用，電腦會直接使用，用來計算它的總力 
            
            if total_tilt != 0:
                if use_mutex:
                    mutex.acquire()
                try:
                    temp = pos
                    pos = temp - total_tilt
                    if total_tilt > 0:
                        player_click_count += total_tilt
                    else:
                        computer_click_count += abs(total_tilt)
                    print_status()
                finally:
                    if use_mutex:
                        mutex.release()

#UI介面
def draw_shop(mouse_pos):
    #背景
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, 280, H))
    pygame.draw.line(screen, (100, 100, 100), (280, 0), (280, H), 3)
    
    screen.blit(font.render(f"Coins: {int(coins)}", True, "black"), (20, 20))
    screen.blit(font.render(f"Level: {level}", True, "black"), (20, 50))
    screen.blit(font.render(f"Click Power: {click_power}", True, (0, 0, 150)), (20, 80))
    
    #mutex開關
    mutex_button = pygame.Rect(20, 110, 240, 50)
    button_color = (100, 200, 100) if use_mutex else (200, 100, 100)
    pygame.draw.rect(screen, button_color, mutex_button, border_radius=10)
    status_text = "MUTEX: ON" if use_mutex else "MUTEX: OFF"
    screen.blit(font.render(status_text, True, "white"), (55, 125))

    #商店按鈕
    buttons = {
        "gear": pygame.Rect(20, 180, 240, 60),
        "gear2": pygame.Rect(20, 250, 240, 60),
        "gear3": pygame.Rect(20, 320, 240, 60),
        "gear4": pygame.Rect(20, 390, 240, 60),
        "gear5": pygame.Rect(20, 460, 240, 60),
        "upgrade_click": pygame.Rect(20, 530, 240, 60),
        "mutex_toggle": mutex_button
    }
    
    for key, rect in buttons.items():
        if key == "gear":
            color = (180, 255, 180) if int(coins) >= 50 else (210, 210, 210)
        elif key == "gear2":
            color = (180, 255, 180) if int(coins) >= 60 else (210, 210, 210)
        elif key == "gear3":
            color = (180, 255, 180) if int(coins) >= 70 else (210, 210, 210)
        elif key == "gear4":
            color = (180, 255, 180) if int(coins) >= 80 else (210, 210, 210)
        elif key == "gear5":
            color = (180, 255, 180) if int(coins) >= 100 else (210, 210, 210)
        elif key == "upgrade_click":
            color = (180, 255, 180) if int(coins) >= 150 else (210, 210, 210)
        elif key == "mutex_toggle":
            continue  
        pygame.draw.rect(screen, color, rect, border_radius=5)

    
    # 文字
    screen.blit(font.render("Buy Gear ($50)", True, "black"), (40, 200))
    screen.blit(font.render("Buy Gear 2 ($60)", True, "black"), (40, 270))
    screen.blit(font.render("Buy Gear 3 ($70)", True, "black"), (40, 340))
    screen.blit(font.render("Buy Gear 4 ($80)", True, "black"), (40, 410))
    screen.blit(font.render("Buy Gear 5 ($100)", True, "black"), (40, 480))
    screen.blit(font.render("Upgrade Click ($150)", True, "black"), (40, 540))
    
    return buttons

def run_game():
    global pos, player_click_count, computer_click_count, game_over, coins, level, gear_power, click_power, use_mutex, gear_power_2, gear_power_3, gear_power_4, gear_power_5, card_system, computer_difficulty_multi
    
    player_stick = Stickman("Player", H)
    com_stick = Stickman("Computer", H)
    
    # 初始化抽卡系統
    card_system = CardSystem(screen, W, H)
    
    # 根據難度設定電腦速度
    if difficulty == "easy":
        computer_difficulty_multi = 0.7
    elif difficulty == "normal":
        computer_difficulty_multi = 1.0
    elif difficulty == "hard":
        computer_difficulty_multi = 1.5
    
    #thread
    threading.Thread(target=computer, daemon=True).start()
    threading.Thread(target=gears, daemon=True).start()
    threading.Thread(target=gears_2, daemon=True).start()
    threading.Thread(target=gears_3, daemon=True).start()
    threading.Thread(target=gears_4, daemon=True).start()
    threading.Thread(target=gears_5, daemon=True).start()
    threading.Thread(target=tilt_power, daemon=True).start()

    running = True
    win_delay = 0
    
    while running:
        screen.fill((255, 255, 255))
        mouse_pos = pygame.mouse.get_pos()
        dt = clock.tick(30) / 1000.0

        center_x = 640
        rope_y = H // 2
        win_line_dist = 250 

        # 勝負線
        pygame.draw.line(screen, (220, 220, 220), (center_x, 100), (center_x, 500), 2)
        pygame.draw.line(screen, (255, 100, 100), (center_x - win_line_dist, 100), (center_x - win_line_dist, 500), 3)
        pygame.draw.line(screen, (100, 100, 255), (center_x + win_line_dist, 100), (center_x + win_line_dist, 500), 3)

        # 繩子與角色位移
        visual_pos = pos * 10
        pygame.draw.line(screen, (100, 50, 0), (center_x - 200 + visual_pos, rope_y), (center_x + 200 + visual_pos, rope_y), 5)
        pygame.draw.circle(screen, (255, 0, 0), (center_x + visual_pos, rope_y), 10)
        
        player_stick.draw_stickman(center_x - 150 + visual_pos, rope_y - 45, screen)
        com_stick.draw_stickman(center_x + 150 + visual_pos, rope_y - 45, screen)

        #置頂
        buttons = draw_shop(mouse_pos)
        
        # 玩家卡
        card_buttons = card_system.draw_player_cards(mouse_pos, 510)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                #mutex lock 開關
                if buttons["mutex_toggle"].collidepoint(mouse_pos):
                    use_mutex = not use_mutex
                
                # gear
                elif buttons["gear"].collidepoint(mouse_pos) and coins >= 50:
                    coins -= 50
                    gear_power += 1
                elif buttons["gear2"].collidepoint(mouse_pos) and coins >= 60:
                    coins -= 60
                    gear_power_2 += 1
                elif buttons["gear3"].collidepoint(mouse_pos) and coins >= 70:
                    coins -= 70
                    gear_power_3 += 1
                elif buttons["gear4"].collidepoint(mouse_pos) and coins >= 80:
                    coins -= 80
                    gear_power_4 += 1
                elif buttons["gear5"].collidepoint(mouse_pos) and coins >= 100:
                    coins -= 100
                    gear_power_5 += 1
                elif buttons["upgrade_click"].collidepoint(mouse_pos) and coins >= 150:
                    coins -= 150
                    click_power += 1
                
                # 使用卡牌
                else:
                    card_used = False
                    for card_rect, card in card_buttons:
                        if card_rect.collidepoint(mouse_pos):
                            card_system.use_card(card)
                            card_used = True
                            break
                    
                    if not card_used:
                        # 點擊區域
                        if mouse_pos[0] > 280: 
                            # 是否被麻痺
                            if card_system and card_system.player_paralyzed:
                                continue
                                
                            if use_mutex: 
                                mutex.acquire() #因為多個執行續在搶pos所以上鎖
                            try:
                                temp = pos
                                pos = temp - click_power
                                player_click_count += click_power 
                                multiplier = card_system.get_coin_multiplier("player")
                                coins += 1 * multiplier
                                print_status()
                            finally:
                                if use_mutex: 
                                    mutex.release()

        #勝負判定
        if pos <= -25: # 玩家贏
            if not game_over:
                game_over = True
                win_delay = 2.0
                
                # 效果消失
                card_system.next_level()
                
                # 5關玩家抽卡
                if level % 5 == 0:
                    card = card_system.draw_card("player")
                    card_system.show_draw(card)
                    
                    # Debuff 抽到直接用，Buff 手牌
                    if card.type == "debuff":
                        card_system.use_card(card)
                
            screen.blit(big_font.render(f"NEXT LEVEL {level + 1}", True, (0, 150, 0)), (400, H//2 - 50))
            if win_delay > 0:
                win_delay -= dt
                if win_delay <= 0:
                    # 重置數據
                    level += 1
                    pos = 0.0
                    player_click_count = 0
                    computer_click_count = 0
                    game_over = False
                    
                    # 重啟thread
                    threading.Thread(target=computer, daemon=True).start()
                    threading.Thread(target=gears, daemon=True).start()
                    threading.Thread(target=gears_2, daemon=True).start()
                    threading.Thread(target=gears_3, daemon=True).start()
                    threading.Thread(target=gears_4, daemon=True).start()
                    threading.Thread(target=gears_5, daemon=True).start()
                    threading.Thread(target=tilt_power, daemon=True).start()
                    
                    print(f"LEVEL {level}")

        elif pos >= 25: # 電腦贏
            screen.blit(big_font.render("LOSE", True, (255, 0, 0)), (350, H//2 - 50))
            game_over = True

        pygame.display.flip()

if __name__ == "__main__":
    menu = MainMenu(screen, W, H)
    result, selected_difficulty = menu.main_menu()
    if result == "START":
        difficulty = selected_difficulty
        run_game()
    pygame.quit()