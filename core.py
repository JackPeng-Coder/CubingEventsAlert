import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import messagebox, font
import os

# 设置需要标红的省份
HIGHLIGHTED_PROVINCES = ["广东"]


# 获取新数据
def get_new_data():
    url = "https://cubing.com/competition?year=&type=&province=&event="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    new_list = []

    results = soup.find_all("tr")

    for i in results:
        sub_soup = BeautifulSoup(str(i), "html.parser")
        sub_results = sub_soup.find_all("td")
        sub_list = []
        for j in sub_results:
            sub_list.append(j.text.replace("天小时分秒", ""))
        new_list.append(sub_list)

    return new_list


# 读取已有数据
def read_existing_data():
    if os.path.exists("data.json"):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    else:
        return []


# 比较数据并找出新赛事
def find_new_competitions(new_data, old_data):
    new_competitions = []

    # 创建一个集合，包含所有已有赛事的名称
    existing_names = set()
    for comp in old_data:
        if len(comp) >= 2:  # 确保有足够的元素
            existing_names.add(comp[1])  # 赛事名称在第二个位置

    # 查找新赛事
    for comp in new_data:
        if (
            len(comp) >= 2 and comp[1] not in existing_names and comp[1].strip()
        ):  # 确保有足够的元素且名称不为空
            new_competitions.append(comp)

    return new_competitions


# 显示美化的弹窗
def show_popup(new_competitions):
    if not new_competitions:
        return

    root = tk.Tk()
    root.title("魔方赛事更新提醒")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")

    title_font = font.Font(family="Microsoft YaHei", size=14, weight="bold")
    header_font = font.Font(family="Microsoft YaHei", size=12, weight="bold")
    content_font = font.Font(family="Microsoft YaHei", size=10)

    title_label = tk.Label(
        root, text="发现新赛事！", font=title_font, bg="#f0f0f0", fg="#FF5722"
    )
    title_label.pack(pady=(20, 10))

    frame_canvas = tk.Frame(root)
    frame_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(frame_canvas, bg="#f0f0f0", highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def resize_frame(event):
        canvas_width = event.width
        canvas.itemconfig(window_id, width=canvas_width)

    canvas.bind("<Configure>", resize_frame)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    for i, comp in enumerate(new_competitions):
        if len(comp) >= 5:
            # 判断是否为需要标红的省份
            is_highlighted = comp[2].strip() in HIGHLIGHTED_PROVINCES
            card_bg = "#fff0f0" if is_highlighted else "white"
            name_fg = "#e53935" if is_highlighted else "#2196F3"
            border_color = "#e53935" if is_highlighted else "#cccccc"
            comp_frame = tk.Frame(
                scrollable_frame,
                bg=card_bg,
                bd=2,
                relief=tk.GROOVE,
                highlightbackground=border_color,
                highlightcolor=border_color,
                highlightthickness=2 if is_highlighted else 1,
            )
            comp_frame.pack(fill=tk.X, padx=10, pady=5, ipadx=5, ipady=5)
            name_label = tk.Label(
                comp_frame, text=comp[1], font=header_font, bg=card_bg, fg=name_fg
            )
            name_label.pack(anchor="w", padx=10, pady=(5, 0))
            date_frame = tk.Frame(comp_frame, bg=card_bg)
            date_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
            date_title = tk.Label(
                date_frame,
                text="日期:",
                font=content_font,
                bg=card_bg,
                fg="#757575",
                width=8,
                anchor="w",
            )
            date_title.pack(side=tk.LEFT)
            date_value = tk.Label(
                date_frame, text=comp[0], font=content_font, bg=card_bg
            )
            date_value.pack(side=tk.LEFT)
            province_frame = tk.Frame(comp_frame, bg=card_bg)
            province_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
            province_title = tk.Label(
                province_frame,
                text="省份:",
                font=content_font,
                bg=card_bg,
                fg="#757575",
                width=8,
                anchor="w",
            )
            province_title.pack(side=tk.LEFT)
            province_value = tk.Label(
                province_frame,
                text=comp[2],
                font=content_font,
                bg=card_bg,
                fg="#e53935" if is_highlighted else "black",
            )
            province_value.pack(side=tk.LEFT)
            city_frame = tk.Frame(comp_frame, bg=card_bg)
            city_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
            city_title = tk.Label(
                city_frame,
                text="城市:",
                font=content_font,
                bg=card_bg,
                fg="#757575",
                width=8,
                anchor="w",
            )
            city_title.pack(side=tk.LEFT)
            city_value = tk.Label(
                city_frame, text=comp[3], font=content_font, bg=card_bg
            )
            city_value.pack(side=tk.LEFT)
            location_frame = tk.Frame(comp_frame, bg=card_bg)
            location_frame.pack(fill=tk.X, padx=10, pady=(5, 5))
            location_title = tk.Label(
                location_frame,
                text="地点:",
                font=content_font,
                bg=card_bg,
                fg="#757575",
                width=8,
                anchor="w",
            )
            location_title.pack(side=tk.LEFT, anchor="nw")
            location_value = tk.Label(
                location_frame,
                text=comp[4],
                font=content_font,
                bg=card_bg,
                anchor="w",
                justify=tk.LEFT,
            )
            location_value.pack(side=tk.LEFT, fill=tk.X, expand=True)
            # 设置省略号效果
            location_value.bind(
                "<Configure>",
                lambda e, lbl=location_value, txt=comp[4]: _set_ellipsis(lbl, txt),
            )
    close_button = tk.Button(
        root,
        text="关闭",
        command=root.destroy,
        bg="#1976D2",
        fg="white",
        font=content_font,
        width=10,
        activebackground="#1565C0",
        activeforeground="white",
    )
    close_button.pack(pady=(5, 20))
    # 仅有一个赛事时禁用滚动条和滚轮
    if len(new_competitions) <= 1:
        scrollbar.pack_forget()
        canvas.unbind_all("<MouseWheel>")
    root.mainloop()


# 主函数
def main():
    new_data = get_new_data()
    old_data = read_existing_data()
    new_competitions = find_new_competitions(new_data, old_data)
    if new_competitions:
        show_popup(new_competitions)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)


# 省略号处理函数
def _set_ellipsis(label, text):
    f = label.cget("font")
    max_width = label.winfo_width()
    if max_width <= 0:
        return
    temp = text
    while label.winfo_reqwidth() > max_width and len(temp) > 1:
        temp = temp[:-1]
        label.config(text=temp + "...")
    if label.cget("text") != text and label.winfo_reqwidth() <= max_width:
        label.config(text=temp + "...")
    elif label.cget("text") != text:
        label.config(text=text)


if __name__ == "__main__":
    main()
