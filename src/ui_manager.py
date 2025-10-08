# src/ui_manager.py

import customtkinter as ctk
from PIL import Image
import pystray
from tkcalendar import Calendar
from datetime import date

class UIManager:
    def __init__(self, icon_path, schedule_manager):
        self.icon_path = icon_path
        self.schedule_manager = schedule_manager
        
        # --- UI State ---
        self.selected_date = date.today()
        
        # --- UI Widgets ---
        self.schedule_display_frame = None
        self.hour_picker = None
        self.minute_picker = None
        self.title_entry = None
        self.calendar = None
        
        self.window = self._create_window()
        self.icon = self._create_icon()

    def _create_window(self):
        ctk.set_appearance_mode("System")  # Light, Dark, System
        ctk.set_default_color_theme("blue")

        window = ctk.CTk()
        window.title("行程提醒")
        window.geometry("400x650")

        # --- Layout ---
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)

        # --- Frames ---
        self._setup_calendar_frame(window)
        self._setup_schedule_display_frame(window)
        self._setup_input_frame(window)

        window.protocol("WM_DELETE_WINDOW", self._hide_window)
        window.withdraw()
        return window

    def _setup_calendar_frame(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.calendar = Calendar(frame, selectmode='day', date_pattern='y-mm-dd')
        self.calendar.pack(expand=True, fill='both')
        self.calendar.bind("<<CalendarSelected>>", self._on_date_select)

    def _setup_schedule_display_frame(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        self.schedule_display_frame = ctk.CTkScrollableFrame(frame, label_text=f"{self.selected_date.strftime('%Y-%m-%d')} 的行程")
        self.schedule_display_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    def _setup_input_frame(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        frame.grid_columnconfigure(1, weight=1)
        
        hours = [f"{h:02d}" for h in range(24)]
        minutes = [f"{m:02d}" for m in range(0, 60, 5)]

        ctk.CTkLabel(frame, text="時間:").grid(row=0, column=0, padx=5, pady=5)
        self.hour_picker = ctk.CTkOptionMenu(frame, values=hours)
        self.hour_picker.grid(row=0, column=1, padx=(0,5), pady=5, sticky="w")
        self.minute_picker = ctk.CTkOptionMenu(frame, values=minutes)
        self.minute_picker.grid(row=0, column=2, padx=(0,5), pady=5, sticky="w")
        
        ctk.CTkLabel(frame, text="標題:").grid(row=1, column=0, padx=5, pady=5)
        self.title_entry = ctk.CTkEntry(frame, placeholder_text="輸入行程標題...")
        self.title_entry.grid(row=1, column=1, columnspan=2, padx=(0,5), pady=5, sticky="ew")
        
        add_button = ctk.CTkButton(frame, text="新增行程", command=self._handle_add_schedule)
        add_button.grid(row=2, column=0, columnspan=3, pady=10)

    def _on_date_select(self, event=None):
        self.selected_date = self.calendar.get_date()
        self.selected_date = date.fromisoformat(self.selected_date)
        self._update_window_content()

    def _update_window_content(self):
        for widget in self.schedule_display_frame.winfo_children():
            widget.destroy()

        self.schedule_display_frame.configure(label_text=f"{self.selected_date.strftime('%Y-%m-%d')} 的行程")
        schedules = self.schedule_manager.load_schedules_for_date(self.selected_date)

        if not schedules:
            ctk.CTkLabel(self.schedule_display_frame, text="本日無行程", text_color="gray").pack(pady=10)
        else:
            for item in schedules:
                item_frame = ctk.CTkFrame(self.schedule_display_frame)
                item_frame.pack(fill='x', pady=4, padx=4)
                
                schedule_text = f"{item.get('time', 'N/A')} - {item.get('title', '無標題')}"
                ctk.CTkLabel(item_frame, text=schedule_text).pack(side='left', padx=10)
                
                delete_button = ctk.CTkButton(
                    item_frame, text="刪除", width=60, fg_color="transparent", border_width=1,
                    command=lambda i=item: self._handle_delete_schedule(i))
                delete_button.pack(side='right', padx=10)

    def _handle_add_schedule(self):
        hour = self.hour_picker.get()
        minute = self.minute_picker.get()
        title = self.title_entry.get().strip()
        
        if not title:
            return
            
        new_schedule = {"time": f"{hour}:{minute}", "title": title}
        self.schedule_manager.add_schedule(self.selected_date, new_schedule)
        
        self.title_entry.delete(0, 'end')
        self._update_window_content()

    def _handle_delete_schedule(self, schedule_to_delete):
        self.schedule_manager.delete_schedule(self.selected_date, schedule_to_delete)
        self._update_window_content()

    def _show_window(self):
        self._on_date_select() # 每次顯示時都更新到最新選擇的日期
        self.window.after(0, self.window.deiconify)
        self.window.after(10, self.window.lift)
        self.window.after(20, lambda: self.window.attributes('-topmost', True))
        self.window.after(30, lambda: self.window.attributes('-topmost', False))
    
    # ... 其餘函式保持不變 ...
    def _hide_window(self):
        self.window.withdraw()

    def _create_icon(self):
        try: image = Image.open(self.icon_path)
        except: image = Image.new('RGB', (64, 64), color='white')
        menu = (
            pystray.MenuItem('顯示行程', self._show_window, default=True),
            pystray.MenuItem('退出', self._on_exit),
        )
        return pystray.Icon("ScheduleReminder", image, "行程提醒", menu)

    def _on_exit(self):
        self.icon.stop()
        self.window.after(0, self.window.destroy)

    def run(self):
        self.window.mainloop()