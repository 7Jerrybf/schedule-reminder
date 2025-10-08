# src/ui_manager.py

import tkinter as tk
from PIL import Image
import pystray

class UIManager:
    def __init__(self, icon_path, schedule_manager): # 新增 schedule_manager 參數
        self.icon_path = icon_path
        self.schedule_manager = schedule_manager # 儲存 schedule_manager 的參考
        self.schedule_labels_frame = None # 用來存放動態標籤的框架
        self.window = self._create_window()
        self.icon = self._create_icon()

    def _create_window(self):
        window = tk.Tk()
        window.title("今日行程")
        window.geometry("300x400")
        window.minsize(200, 200)

        # 建立一個固定的頂部標題
        tk.Label(window, text="您的行程列表：", font=("Arial", 14)).pack(pady=10, padx=20)
        
        # 建立一個專門用來放置行程標籤的框架 (Frame)
        self.schedule_labels_frame = tk.Frame(window)
        self.schedule_labels_frame.pack(fill="both", expand=True, padx=20)

        window.protocol("WM_DELETE_WINDOW", self._hide_window)
        window.withdraw()
        return window

    def _update_window_content(self):
        """
        更新視窗中的行程列表。
        """
        # 1. 清除舊的行程標籤
        for widget in self.schedule_labels_frame.winfo_children():
            widget.destroy()

        # 2. 從 ScheduleManager 載入最新的行程
        schedules = self.schedule_manager.load_schedules()

        # 3. 根據最新的行程資料，建立新的標籤
        if not schedules:
            tk.Label(self.schedule_labels_frame, text="今日無行程", fg="gray").pack(pady=10)
        else:
            for item in schedules:
                schedule_text = f"- {item.get('time', 'N/A')}  {item.get('title', '無標題')}"
                tk.Label(
                    self.schedule_labels_frame,
                    text=schedule_text,
                    justify=tk.LEFT
                ).pack(anchor="w")

    def _show_window(self):
        self._update_window_content() # *** 關鍵：在顯示視窗前，先更新內容 ***
        self.window.after(0, self.window.deiconify)
        self.window.after(1, self.window.lift)
        self.window.after(2, lambda: self.window.attributes('-topmost', True))
        self.window.after(3, lambda: self.window.attributes('-topmost', False))

    def _hide_window(self):
        self.window.withdraw()

    # ... _create_icon 和 _on_exit 函式保持不變 ...
    def _create_icon(self):
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
        print("正在關閉應用程式...")
        self.icon.stop()
        self.window.after(0, self.window.destroy)

    def run(self):
        print("應用程式UI主迴圈啟動。")
        self.window.mainloop()
        print("應用程式UI主迴圈已結束。")