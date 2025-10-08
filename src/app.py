# src/app.py

import os
import threading
from ui_manager import UIManager

# --- 應用程式設定 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, '..', 'assets', 'icon.png')

def main():
    """
    應用程式主函式。
    """
    # 1. 建立 UI 管理器的實例
    #    這一步也會在主執行緒中建立好隱藏的Tkinter視窗
    ui = UIManager(icon_path=ICON_PATH)

    # 2. 建立並啟動一個背景執行緒來運行系統匣圖示
    #    target=ui.icon.run 表示這個執行緒要去執行 ui.icon.run() 這個函式
    #    daemon=True 確保當主程式結束時，這個背景執行緒也會被強制終止
    icon_thread = threading.Thread(target=ui.icon.run, daemon=True)
    
    print("啟動背景執行緒中的系統匣圖示...")
    icon_thread.start()

    # 3. 在主執行緒中啟動 Tkinter 的事件迴圈
    #    這將會是一個阻塞操作，直到 Tkinter 視窗被銷毀
    ui.run()

if __name__ == "__main__":
    main()