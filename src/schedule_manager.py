# src/schedule_manager.py

import json
import os
from datetime import date

class ScheduleManager:
    def __init__(self, data_path):
        self.data_path = data_path
        if not os.path.exists(self.data_path):
            self._save_all_schedules({})

    def _load_all_schedules(self):
        """
        載入包含所有日期的整個行程資料字典。
        新增了對舊格式資料 (list) 的相容性處理。
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # *** 關鍵的防禦性檢查 ***
                # 如果讀取到的資料是個列表 (舊格式)，則回傳一個空字典，
                # 這樣就不會觸發 AttributeError，並允許程式以新的格式重新開始。
                if isinstance(data, list):
                    print("警告: 偵測到舊版資料格式，將重置為新格式。")
                    return {}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def _save_all_schedules(self, all_schedules):
        """儲存整個行程資料字典。"""
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(all_schedules, f, indent=2, ensure_ascii=False)

    def load_schedules_for_date(self, target_date):
        """載入並回傳指定日期的行程列表。"""
        date_str = target_date.strftime('%Y-%m-%d')
        all_schedules = self._load_all_schedules()
        schedules = all_schedules.get(date_str, [])
        schedules.sort(key=lambda x: x.get('time', ''))
        return schedules

    def add_schedule(self, target_date, new_schedule):
        """在指定日期新增一個行程。"""
        date_str = target_date.strftime('%Y-%m-%d')
        all_schedules = self._load_all_schedules()
        
        if date_str not in all_schedules:
            all_schedules[date_str] = []
            
        all_schedules[date_str].append(new_schedule)
        all_schedules[date_str].sort(key=lambda x: x.get('time', ''))
        self._save_all_schedules(all_schedules)
        print(f"在 {date_str} 新增行程: {new_schedule}")

    def delete_schedule(self, target_date, schedule_to_delete):
        """從指定日期刪除一個行程。"""
        date_str = target_date.strftime('%Y-%m-%d')
        all_schedules = self._load_all_schedules()
        
        if date_str in all_schedules and schedule_to_delete in all_schedules[date_str]:
            all_schedules[date_str].remove(schedule_to_delete)
            # 如果某個日期的行程都刪光了，就從字典中移除該日期
            if not all_schedules[date_str]:
                del all_schedules[date_str]
            self._save_all_schedules(all_schedules)
            print(f"從 {date_str} 刪除行程: {schedule_to_delete}")