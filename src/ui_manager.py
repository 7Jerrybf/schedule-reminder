# src/ui_manager.py

import tkinter as tk
from PIL import Image
import pystray

class UIManager:
    """
    管理所有使用者介面元素，確保執行緒安全。
    """
    def __init__(self, icon_path):
        """
        初始化UI管理器。
        關鍵：在這裡建立視窗物件，以確保它在主執行緒上被建立。
        """
        self.icon_path = icon_path
        self.window = self._create_window()  # 立即建立視窗，然後隱藏
        self.icon = self._create_icon()

    def _create_window(self):
        """
        建立 Tkinter 視窗物件並隱藏。
        """
        window = tk.Tk()
        window.title("今日行程")
        window.geometry("300x400")
        window.minsize(200, 200)

        tk.Label(window, text="您的行程列表：", font=("Arial", 14)).pack(pady=10, padx=20)
        tk.Label(window, text="- 09:00 開會", justify=tk.LEFT).pack(anchor="w", padx=20)
        tk.Label(window, text="- 14:30 專案報告", justify=tk.LEFT).pack(anchor="w", padx=20)

        window.protocol("WM_DELETE_WINDOW", self._hide_window)
        window.withdraw()  # 建立後立刻隱藏
        return window

    def _show_window(self):
        """
        從背景執行緒安全地請求顯示視窗。
        """
        # 使用 .after() 將操作排程到 Tkinter 的主事件迴圈中執行，這是執行緒安全的
        self.window.after(0, self.window.deiconify)
        self.window.after(1, self.window.lift) # 稍微延遲以確保視窗已顯示
        self.window.after(2, lambda: self.window.attributes('-topmost', True))
        self.window.after(3, lambda: self.window.attributes('-topmost', False))
    
    def _hide_window(self):
        """
        隱藏視窗（這個函式由Tkinter主執行緒直接呼叫，所以是安全的）。
        """
        self.window.withdraw()

    def _create_icon(self):
        """
        建立並設定系統匣圖示。
        """
        try:
            image = Image.open(self.icon_path)
        except FileNotFoundError:
            print(f"警告: 找不到圖示檔案於 '{self.icon_path}'。將使用預設圖示。")
            image = Image.new('RGB', (64, 64), color='white')

        menu = (
            pystray.MenuItem('顯示行程', self._show_window, default=True),
            pystray.MenuItem('退出', self._on_exit),
        )

        icon = pystray.Icon("ScheduleReminder", image, "行程提醒", menu)
        return icon

    def _on_exit(self):
        """
        從背景執行緒安全地請求退出應用程式。
        """
        print("正在關閉應用程式...")
        self.icon.stop()
        # 安全地請求銷毀Tkinter視窗
        self.window.after(0, self.window.destroy)

    def run(self):
        """
        啟動應用程式的主迴圈 (Tkinter)。
        系統匣圖示應該在一個單獨的執行緒中運行。
        """
        print("應用程式UI主迴圈啟動。")
        self.window.mainloop()
        print("應用程式UI主迴圈已結束。")