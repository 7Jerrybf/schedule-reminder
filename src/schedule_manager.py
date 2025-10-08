# src/schedule_manager.py

import json
import os

class ScheduleManager:
    def __init__(self, data_path):
        self.data_path = data_path
        if not os.path.exists(self.data_path):
            self._save_schedules([])

    def load_schedules(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                schedules = json.load(f)
            # 確保行程按時間排序
            schedules.sort(key=lambda x: x.get('time', ''))
            return schedules
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_schedules(self, schedules):
        # 在儲存前，確保行程是按時間排序的
        schedules.sort(key=lambda x: x.get('time', ''))
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)

    def add_schedule(self, new_schedule):
        """
        新增一個行程並儲存。

        :param new_schedule: 一個包含 'time' 和 'title' 的字典。
        """
        schedules = self.load_schedules()
        schedules.append(new_schedule)
        self._save_schedules(schedules)
        print(f"行程已新增: {new_schedule}")

    def delete_schedule(self, schedule_to_delete):
        """
        刪除一個指定的行程並儲存。

        :param schedule_to_delete: 要刪除的行程字典。
        """
        schedules = self.load_schedules()
        # 尋找並移除指定的行程
        if schedule_to_delete in schedules:
            schedules.remove(schedule_to_delete)
            self._save_schedules(schedules)
            print(f"行程已刪除: {schedule_to_delete}")
        else:
            print(f"警告: 找不到要刪除的行程: {schedule_to_delete}")