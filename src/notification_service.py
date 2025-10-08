# src/notification_service.py

import threading
import time
from datetime import datetime
from plyer import notification

class NotificationService:
    """
    在背景運行，負責檢查行程並在適當時間發送桌面通知。
    """
    def __init__(self, schedule_manager):
        """
        初始化通知服務。

        :param schedule_manager: ScheduleManager 的實例，用來獲取行程資料。
        """
        self.schedule_manager = schedule_manager
        self._running = False
        self._notified_today = set() # 用來存放今天已提醒過的行程元組 (time, title)
        self._last_check_date = None # 用來偵測日期是否跨天

    def _checker_loop(self):
        """
        背景檢查迴圈，每分鐘執行一次。
        """
        while self._running:
            current_date = datetime.now().date()
            # 如果跨天了，重置已提醒列表
            if self._last_check_date and self._last_check_date != current_date:
                print("新的一天，重置通知列表。")
                self._notified_today.clear()
            self._last_check_date = current_date

            # 格式化目前時間為 "HH:MM"
            current_time_str = datetime.now().strftime('%H:%M')
            
            schedules = self.schedule_manager.load_schedules()

            for item in schedules:
                schedule_time = item.get('time')
                schedule_title = item.get('title')
                schedule_tuple = (schedule_time, schedule_title)

                # 檢查時間是否相符，且今天尚未提醒過
                if schedule_time == current_time_str and schedule_tuple not in self._notified_today:
                    print(f"發送提醒: {schedule_time} - {schedule_title}")
                    
                    # 發送桌面通知
                    notification.notify(
                        title='行程提醒',
                        message=f"{schedule_time} - {schedule_title}",
                        app_name='行程提醒應用程式',
                        timeout=10  # 通知顯示 10 秒
                    )
                    
                    # 將此行程加入到已提醒列表，避免重複提醒
                    self._notified_today.add(schedule_tuple)

            # 等待 60 秒再進行下一次檢查
            time.sleep(60)

    def start(self):
        """
        啟動背景通知服務。
        """
        if self._running:
            return

        print("啟動背景通知服務...")
        self._running = True
        self._last_check_date = datetime.now().date()
        # 建立並啟動一個守護執行緒 (daemon thread)
        self.thread = threading.Thread(target=self._checker_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """
        停止背景通知服務 (目前主要由 daemon=True 自動處理)。
        """
        print("停止背景通知服務...")
        self._running = False