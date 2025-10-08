# src/ui_manager.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image
import pystray
import re

class UIManager:
    """
    管理所有使用者介面元素。
    經過重構，將UI佈局和邏輯分離得更清晰。
    """
    def __init__(self, icon_path, schedule_manager):
        self.icon_path = icon_path
        self.schedule_manager = schedule_manager
        
        self.schedule_labels_frame = None
        self.time_entry = None
        self.title_entry = None
        
        self.window = self._create_window()
        self.icon = self._create_icon()

    def _create_window(self):
        """主視窗的總建立函式，呼叫輔助函式來設定各個區塊。"""
        window = tk.Tk()
        window.title("行程提醒")
        window.geometry("350x500")
        window.minsize(300, 400)

        # 使用輔助函式來建立和佈局UI元件
        self._setup_input_frame(window)
        self._setup_separator(window)
        self._setup_display_frame(window)

        window.protocol("WM_DELETE_WINDOW", self._hide_window)
        window.withdraw()
        return window

    def _setup_input_frame(self, parent_window):
        """設定視窗頂部的輸入區塊（時間、標題、新增按鈕）。"""
        input_frame = tk.Frame(parent_window, pady=10)
        input_frame.pack(fill='x', padx=10)
        
        tk.Label(input_frame, text="時間 (HH:MM):").grid(row=0, column=0, sticky='w')
        self.time_entry = tk.Entry(input_frame, width=10)
        self.time_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="標題:").grid(row=1, column=0, sticky='w', pady=5)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        
        add_button = tk.Button(input_frame, text="新增行程", command=self._handle_add_schedule)
        add_button.grid(row=2, column=1, sticky='e', pady=10)

    def _setup_separator(self, parent_window):
        """在輸入區和顯示區之間建立一條分隔線。"""
        separator = tk.Frame(parent_window, height=2, bd=1, relief='sunken')
        separator.pack(fill='x', padx=5, pady=5)

    def _setup_display_frame(self, parent_window):
        """設定視窗下半部的行程顯示區塊。"""
        tk.Label(parent_window, text="今日行程列表：", font=("Arial", 14)).pack(pady=5)
        self.schedule_labels_frame = tk.Frame(parent_window)
        self.schedule_labels_frame.pack(fill="both", expand=True, padx=10)

    def _update_window_content(self):
        """清除並根據最新資料重新繪製行程列表。"""
        for widget in self.schedule_labels_frame.winfo_children():
            widget.destroy()

        schedules = self.schedule_manager.load_schedules()

        if not schedules:
            tk.Label(self.schedule_labels_frame, text="目前無行程", fg="gray").pack(pady=10)
        else:
            for item in schedules:
                item_frame = tk.Frame(self.schedule_labels_frame)
                item_frame.pack(fill='x', pady=2)
                
                schedule_text = f"{item.get('time', 'N/A')} - {item.get('title', '無標題')}"
                tk.Label(item_frame, text=schedule_text, justify=tk.LEFT).pack(side='left', anchor="w")
                
                delete_button = tk.Button(
                    item_frame, text="刪除", fg="red",
                    command=lambda current_item=item: self._handle_delete_schedule(current_item)
                )
                delete_button.pack(side='right')

    def _validate_time_format(self, time_str):
        """增強的時間驗證函式，不僅檢查格式，還檢查數值範圍。"""
        if not re.match(r'^\d{2}:\d{2}$', time_str):
            messagebox.showwarning("格式錯誤", "時間格式應為 HH:MM，例如 09:30。")
            return False
        try:
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                messagebox.showwarning("數值無效", "小時數必須在 00-23 之間，\n分鐘數必須在 00-59 之間。")
                return False
        except ValueError:
            # 這通常不會發生，因為 regex 已經過濾了非數字字符
            messagebox.showerror("內部錯誤", "時間轉換失敗。")
            return False
        return True

    def _handle_add_schedule(self):
        """處理新增按鈕的點擊事件，包含更完善的驗證。"""
        time_str = self.time_entry.get().strip()
        title_str = self.title_entry.get().strip()

        if not self._validate_time_format(time_str):
            return
        if not title_str:
            messagebox.showwarning("內容為空", "行程標題不可為空。")
            return

        new_schedule = {'time': time_str, 'title': title_str}
        self.schedule_manager.add_schedule(new_schedule)
        
        self.time_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.time_entry.focus_set() # 將游標焦點移回時間輸入框
        
        self._update_window_content()

    def _handle_delete_schedule(self, schedule_to_delete):
        """處理刪除按鈕的點擊事件。"""
        self.schedule_manager.delete_schedule(schedule_to_delete)
        self._update_window_content()

    # ... 其餘函式 (_show_window, _hide_window, _create_icon, _on_exit, run) 保持不變 ...
    def _show_window(self):
        self._update_window_content()
        self.window.after(0, self.window.deiconify)
        self.window.after(1, self.window.lift)
        self.window.after(2, lambda: self.window.attributes('-topmost', True))
        self.window.after(3, lambda: self.window.attributes('-topmost', False))

    def _hide_window(self):
        self.window.withdraw()

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