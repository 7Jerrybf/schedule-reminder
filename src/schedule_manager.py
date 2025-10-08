# src/schedule_manager.py

import json
import os

class ScheduleManager:
    """
    負責處理所有與行程資料相關的操作，例如讀取和儲存。
    """
    def __init__(self, data_path):
        """
        初始化行程管理器。

        :param data_path: 行程資料檔案 (例如 schedules.json) 的路徑。
        """
        self.data_path = data_path
        # 如果資料檔案不存在，建立一個空的
        if not os.path.exists(self.data_path):
            self._save_schedules([])

    def load_schedules(self):
        """
        從 JSON 檔案讀取並回傳行程列表。
        """
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                schedules = json.load(f)
            return schedules
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果檔案遺失或格式錯誤，回傳一個空列表以避免程式崩潰
            return []

    def _save_schedules(self, schedules):
        """
        將行程列表寫入 JSON 檔案 (私有輔助函式)。
        """
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(schedules, f, indent=2, ensure_ascii=False)