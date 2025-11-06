import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.clock import Clock

# 註冊你下載的字體（確保 fonts 資料夾內有對應檔案）
LabelBase.register(name="POP", fn_regular="font/HachiMaruPop-Regular.ttf")
LabelBase.register(name="新細明體", fn_regular="font/NotoSansTC-Light.ttf")
LabelBase.register(name="馬克筆", fn_regular="font/LXGWMarkerGothic-Regular.ttf")
LabelBase.register(name="標楷體", fn_regular="font/UoqMunThenKhung-Regular.ttf")

DATA_PATH = "data/notes.json"
os.makedirs("data", exist_ok=True)

class StickyNote(BoxLayout):
    #便利貼一開始的預設值
    text = StringProperty("")
    font_color = ListProperty([0, 0, 0, 1])    # 字體顏色:黑色
    bg_color = ListProperty([1, 0.9, 0.9, 1])  # 背景顏色:淡粉色
    font_name = StringProperty("新細明體")     # 字型:新細明體
    font_color_name = StringProperty("黑")     # 字體顏色名稱
    bg_color_name = StringProperty("淡粉")     # 背景顏色名稱
    content = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.adjust_height, 0)

    def adjust_height(self, *args):
        # 自動調整高度
        content = self.ids.get('content')
        if content:
            content.height = content.minimum_height
            self.height = self.minimum_height

class AnyNote(App):
    ui_font = StringProperty("新細明體")    # 統一字體
    notes = []

    def build(self):
        self.load_notes()
        return Builder.load_file("stickynote.kv")

    def load_notes(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                self.notes = json.load(f)
        else:
            self.notes = []

    def save_notes(self):
        notes_data = []
        for note in self.root.ids.note_container.children[::-1]:
            notes_data.append({
                "text": note.text,
                "font_color": note.font_color,
                "bg_color": note.bg_color,
                "font_name": note.font_name,
                "font_color_name": note.font_color_name,
                "bg_color_name": note.bg_color_name
            })
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(notes_data, f, ensure_ascii=False, indent=2)

    def add_note(self):
        new_note = StickyNote()
        self.root.ids.note_container.add_widget(new_note)
        self.save_notes()

    def delete_note(self, note):
        self.root.ids.note_container.remove_widget(note)
        self.save_notes()

    def get_font_color(self, name):
        return {
            "黑": (0, 0, 0, 1),
            "紅": (1, 0, 0, 1),
            "藍": (0, 0, 1, 1)
        }.get(name, (0, 0, 0, 1))

    def get_bg_color(self, name):
        return {
            "淡粉": (1, 0.9, 0.9, 1),
            "櫻花粉": (1, 0.8, 0.86, 1),
            "桃粉": (1, 0.7, 0.8, 1),
            "淡綠": (0.85, 1, 0.85, 1),
            "藍灰": (0.7, 0.75, 0.85, 1),
            "米白": (1, 1, 0.9, 1)
        }.get(name, (1, 0.9, 0.9, 1))

    def on_start(self):
        for note_data in self.notes:
            note = StickyNote(
                text=note_data.get("text", ""),
                font_color=note_data.get("font_color", [0, 0, 0, 1]),
                bg_color=note_data.get("bg_color", [1, 0.9, 0.9, 1]),
                font_name=note_data.get("font_name", "新細明體"),
                font_color_name=note_data.get("font_color_name", "黑"),
                bg_color_name=note_data.get("bg_color_name", "淡粉")
            )
            self.root.ids.note_container.add_widget(note)

AnyNote().run()
