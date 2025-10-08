# src/app.py

import os
import threading
from ui_manager import UIManager
from schedule_manager import ScheduleManager
from notification_service import NotificationService # 匯入新的服務

# --- 應用程式設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets')
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

ICON_PATH = os.path.join(ASSETS_DIR, 'icon.png')
SCHEDULE_DATA_PATH = os.path.join(DATA_DIR, 'schedules.json')

def main():
    """
    應用程式主函式。
    """
    # 1. 建立資料管理器的實例
    schedule_manager = ScheduleManager(data_path=SCHEDULE_DATA_PATH)

    # 2. 建立並啟動通知服務
    notification_service = NotificationService(schedule_manager=schedule_manager)
    notification_service.start() # 在 UI 啟動前就開始在背景運行

    # 3. 建立 UI 管理器的實例
    ui = UIManager(
        icon_path=ICON_PATH,
        schedule_manager=schedule_manager
    )

    # 4. 建立並啟動系統匣圖示的背景執行緒
    icon_thread = threading.Thread(target=ui.icon.run, daemon=True)
    icon_thread.start()

    # 5. 在主執行緒中啟動 Tkinter 的事件迴圈
    ui.run()

if __name__ == "__main__":
    main()