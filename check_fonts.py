# check_fonts.py
import tkinter
from tkinter import font

# 建立一個暫時的 Tkinter 根視窗 (不會顯示出來)
root = tkinter.Tk()

# 獲取系統上所有可用的字體家族名稱
font_families = font.families()

# 為了方便查看，將字體列表寫入一個文字檔
with open("fonts_list.txt", "w", encoding="utf-8") as f:
    print("正在將您系統上的所有字體名稱寫入 fonts_list.txt ...")
    for family in sorted(font_families):
        f.write(family + "\n")
        print(family)

print("\n完成！請打開專案目錄下的 fonts_list.txt 檔案查看所有可用字體。")

# 關閉暫時的視窗
root.destroy()