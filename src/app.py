# src/app.py

import os
import threading
from ui_manager import UIManager
from schedule_manager import ScheduleManager # 匯入新的類別

# --- 應用程式設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data') # 新增 data 資料夾路徑

ICON_PATH = os.path.join(ASSETS_DIR, 'icon.png')
SCHEDULE_DATA_PATH = os.path.join(DATA_DIR, 'schedules.json') # 新增資料檔案路徑

def main():
    """
    應用程式主函式。
    """
    # 1. 建立資料管理器的實例
    schedule_manager = ScheduleManager(data_path=SCHEDULE_DATA_PATH)

    # 2. 建立 UI 管理器的實例，並將資料管理器傳遞給它
    ui = UIManager(
        icon_path=ICON_PATH,
        schedule_manager=schedule_manager # 傳入 schedule_manager
    )

    # 3. 建立並啟動背景執行緒來運行系統匣圖示
    icon_thread = threading.Thread(target=ui.icon.run, daemon=True)
    icon_thread.start()

    # 4. 在主執行緒中啟動 Tkinter 的事件迴圈
    ui.run()

if __name__ == "__main__":
    main()