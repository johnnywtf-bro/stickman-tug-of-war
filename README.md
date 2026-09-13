# Tug of War Stickman Game

一個使用 Python 與 Pygame 製作的火柴人拔河小遊戲。玩家透過點擊拉動繩子、購買自動拉力齒輪、使用卡牌效果，和電腦進行拔河對戰。

## 功能

- 主選單與難度選擇：easy、normal、hard
- 玩家點擊拉繩，電腦由背景執行緒自動出力
- 商店升級：購買多種 Gear、自動增加拉力、升級點擊力量
- 卡牌系統：金幣倍率、拉力傾斜、麻痺、清除負面效果
- Mutex 開關：可以展示 race condition 與互斥鎖的差異

## 安裝

建議使用 Python 3.11 以上版本。

```bash
pip install -r requirements.txt
```

## 執行

```bash
python game.py
```

## 操作方式

- 點擊遊戲區域拉繩
- 左側商店可購買 Gear 或升級 Click Power
- 點擊 `MUTEX` 按鈕切換互斥鎖
- 每 5 關會抽一張卡牌，玩家可點擊手牌使用 buff 卡

## 專案檔案

- `game.py`：遊戲主程式與主要流程
- `main_menu.py`：主選單與難度選擇
- `stickman.py`：火柴人繪製
- `card.py`：卡牌系統

## GitHub 上傳建議

這個 repository 建議只放正式版原始碼與必要說明。`__pycache__/`、備份資料夾、期末報告影片等已加入 `.gitignore`，避免把暫存檔或大型檔案一起上傳。
