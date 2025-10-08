# src/notification_service.py

import threading
import time
from datetime import datetime
from plyer import notification

class NotificationService:
    def __init__(self, schedule_manager):
        self.schedule_manager = schedule_manager
        self._running = False
        self._notified_today = set()

    def _checker_loop(self):
        while self._running:
            today = datetime.now().date()
            current_time_str = datetime.now().strftime('%H:%M')
            
            # 每天午夜重置已提醒列表
            if current_time_str == "00:00":
                self._notified_today.clear()

            # 只載入今天的行程
            schedules_today = self.schedule_manager.load_schedules_for_date(today)

            for item in schedules_today:
                schedule_tuple = (item.get('time'), item.get('title'))

                if item.get('time') == current_time_str and schedule_tuple not in self._notified_today:
                    print(f"發送提醒: {item.get('time')} - {item.get('title')}")
                    notification.notify(
                        title=f'行程提醒: {item.get("time")}',
                        message=item.get("title"),
                        app_name='行程提醒應用程式',
                        timeout=15
                    )
                    self._notified_today.add(schedule_tuple)

            time.sleep(60)

    def start(self):
        if not self._running:
            print("啟動背景通知服務...")
            self._running = True
            self.thread = threading.Thread(target=self._checker_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self._running = False