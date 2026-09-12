# -*- coding: utf-8 -*-
"""
PVZ2脚本 Kivy GUI版本 v3.0
完整分类菜单 + 所有功能按钮 + 输出日志
"""
import os
import sys
import re
import threading
import queue
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.config import Config
from kivy.core.text import LabelBase

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', '1')

from kivy.utils import platform
if platform == 'android':
    FONT_PATH = 'msyh.ttc'
    SCRIPT_PATH = 'PVZ3.5原版.py'
else:
    FONT_PATH = r'C:\Windows\Fonts\msyh.ttc'
    SCRIPT_PATH = r'C:\Users\33961\Desktop\PVZ3.5原版.py'

if os.path.exists(FONT_PATH):
    LabelBase.register(name='ChineseFont', fn_regular=FONT_PATH)
    LabelBase.register(name='Roboto', fn_regular=FONT_PATH)

CATEGORIES = {
    "日常": [
        ("部分日常", "1\n1"),
        ("植物探险", "1\n2"),
        ("超Z排行榜", "1\n3"),
        ("每月签到全领", "1\n4"),
        ("兑换码领取", "1\n5"),
        ("秘宝抽奖", "1\n6"),
        ("查看存档信息", "1\n7"),
    ],
    "一次性": [
        ("世界关卡钻石", "2\n1"),
        ("三神器领取", "2\n2"),
        ("世界困难装扮", "2\n3"),
        ("世界解锁植物", "2\n4"),
        ("原木世界任务", "2\n5"),
        ("植物图鉴钻石", "2\n6"),
        ("星星兑换", "2\n7"),
        ("游戏天数领奖", "2\n8"),
    ],
    "双人": [
        ("双人宗师", "3\n1"),
        ("双人周任务", "3\n2"),
        ("双人排位奖励", "3\n3"),
        ("双人僵尸升阶", "3\n4"),
        ("基因抽取升级", "3\n5"),
        ("双人胜败查看", "3\n6"),
        ("双人转盘抽取", "3\n7"),
    ],
    "回忆": [
        ("回忆之旅一键", "4\n1"),
        ("回忆成就领取", "4\n2"),
        ("回忆商店购买", "4\n3"),
        ("回忆小游戏全通", "4\n4"),
        ("回忆小游戏成就", "4\n5"),
    ],
    "追击": [
        ("追击刷14w分", "5\n1"),
        ("钻石购买电池", "5\n2"),
        ("零分刷僵王", "5\n3"),
        ("潘追任务奖励", "5\n4"),
        ("查看追击排名", "5\n5"),
        ("追击商店购买", "5\n6"),
    ],
    "无尽": [
        ("刷无尽分", "6\n1"),
        ("刷无尽币", "6\n2"),
        ("无尽币查询", "6\n3"),
        ("无尽广告重置", "6\n4"),
        ("无尽商店购买", "6\n5"),
        ("无尽周任务", "6\n6"),
    ],
    "秘境": [
        ("黄瓜森林第一章", "7\n1"),
        ("黄瓜森林第二章", "7\n2"),
        ("周年秘境满星", "7\n3"),
        ("Z公司秘境", "7\n4"),
        ("地宫秘境1", "7\n5"),
        ("地宫秘境2", "7\n6"),
    ],
    "庭院": [
        ("查看创建关卡", "8\n1"),
        ("庭院点赞", "8\n2"),
        ("庭院商店购买", "8\n3"),
    ],
    "聚宝盆": [
        ("币子经验领取", "9\n1"),
        ("聚宝盆商店", "9\n2"),
    ],
    "砸罐": [
        ("砸罐任务领取", "10\n1"),
        ("砸罐", "10\n2"),
    ],
    "晚会": [
        ("大作战领任务", "11\n1"),
    ],
    "僵局": [
        ("僵局逃脱一键", "12\n1"),
    ],
    "同游": [
        ("同游任务领取", "13\n1"),
        ("同游商店购买", "13\n2"),
    ],
    "响叮当": [
        ("响叮当低保", "14\n1"),
        ("响叮当刷分", "14\n2"),
        ("僵尸清除领奖", "14\n3"),
        ("年兽刷伤", "14\n4"),
    ],
    "限时": [
        ("戴夫厨房60钻", "15\n1"),
        ("破罐大师", "15\n2"),
        ("戴夫宝藏", "15\n3"),
        ("圣诞袜领取", "15\n4"),
        ("问卷调查", "15\n5"),
        ("红水晶商店", "15\n6"),
        ("欢乐购购买", "15\n7"),
        ("七日指南", "15\n8"),
        ("超装活动", "15\n9"),
        ("心愿团购", "15\n10"),
        ("知识问答", "15\n11"),
    ],
    "家族": [
        ("刷家族数值", "16\n1"),
        ("刷具体词条", "16\n2"),
        ("家族数值自查", "16\n3"),
    ],
    "转基因": [
        ("植物碎片转基因", "17\n1"),
        ("植物一键升阶", "17\n2"),
        ("装扮激活转基因", "17\n3"),
    ],
    "存档": [
        ("消除虚拟物品", "18\n1"),
        ("注入超级挂件", "18\n2"),
        ("满星通关", "18\n3"),
        ("开启豌豆共生", "18\n4"),
        ("注入1.3亿金币", "18\n5"),
        ("修改黄瓜30根", "18\n6"),
    ],
    "令营": [
        ("令营任务全领", "19\n1"),
        ("令营转盘领取", "19\n2"),
    ],
    "常用": [
        ("一键日常", "31"),
        ("批量养号", "32"),
        ("僵博挑战", "20"),
        ("抽红包", "21"),
        ("趣味竞赛", "22"),
        ("周年之约", "23"),
        ("时空寻宝", "24"),
        ("潘妮课堂", "25"),
        ("回归有礼", "26"),
        ("戴夫杯", "27"),
        ("远征之门", "28"),
        ("植物培育", "29"),
        ("僵尸清除", "30"),
    ],
    "登录": [
        ("官服登录", "33\n1\n"),
        ("tap登录", "33\n1\n2"),
        ("好游快爆登录", "33\n1\n3"),
        ("努比亚红魔登录", "33\n1\n4"),
        ("4399登录", "33\n1\n5"),
        ("抓包响应登录", "33\n2"),
        ("第三方登录", "33\n3"),
    ],
}

ANSI_PATTERN = re.compile(r'\x1b\[([0-9;]*)m')
BASIC_COLORS = {
    '30': '000000', '31': 'ff4444', '32': '44ff44', '33': 'ffff44',
    '34': '4488ff', '35': 'ff44ff', '36': '44ffff', '37': 'ffffff',
    '90': '888888', '91': 'ff8888', '92': '88ff88', '93': 'ffff88',
    '94': '8888ff', '95': 'ff88ff', '96': '88ffff', '97': 'ffffff',
}
EXTENDED_COLORS = [
    '000000', '800000', '008000', '808000', '000080', '800080', '008080', 'c0c0c0',
    '808080', 'ff0000', '00ff00', 'ffff00', '0000ff', 'ff00ff', '00ffff', 'ffffff',
]


def ansi_to_kivy_markup(text):
    color_stack = []
    def match_ansi(m):
        codes = m.group(1)
        if codes == '' or codes == '0':
            tags = ''
            while color_stack:
                tags += '[/color]'
                color_stack.pop()
            return tags
        parts = codes.split(';')
        i = 0
        result = ''
        while i < len(parts):
            code = parts[i]
            if code == '38' and i + 2 < len(parts) and parts[i + 1] == '5':
                color_idx = int(parts[i + 2])
                if color_idx < 16:
                    color = EXTENDED_COLORS[color_idx]
                elif color_idx < 232:
                    idx = color_idx - 16
                    r = (idx // 36) * 40 + 55 if idx // 36 > 0 else 0
                    g = ((idx % 36) // 6) * 40 + 55 if (idx % 36) // 6 > 0 else 0
                    b = (idx % 6) * 40 + 55 if idx % 6 > 0 else 0
                    color = f'{r:02x}{g:02x}{b:02x}'
                else:
                    gray = (color_idx - 232) * 10 + 8
                    color = f'{gray:02x}{gray:02x}{gray:02x}'
                result += f'[color={color}]'
                color_stack.append(color)
                i += 3
            elif code in BASIC_COLORS:
                color = BASIC_COLORS[code]
                result += f'[color={color}]'
                color_stack.append(color)
                i += 1
            else:
                i += 1
        return result
    text = ANSI_PATTERN.sub(match_ansi, text)
    while color_stack:
        text += '[/color]'
        color_stack.pop()
    text = re.sub(r' {2,}', lambda m: '\u3000' * len(m.group()), text)
    def is_allowed(c):
        if c in '\n\r\t\u3000 ':
            return True
        if '\u4e00' <= c <= '\u9fff':
            return True
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z':
            return True
        if '0' <= c <= '9':
            return True
        if c in '，。！？、：；""''（）【】《》—…·.,!?;:-\'"()[]<>/\\|@#$%^&*_+=~`':
            return True
        return False
    text = ''.join(c for c in text if is_allowed(c))
    return text


class OutputRedirector:
    def __init__(self, output_queue):
        self.output_queue = output_queue
        self.buffer = ''
    def write(self, text):
        self.buffer += text
        if '\n' in text or len(self.buffer) > 1000:
            colored = ansi_to_kivy_markup(self.buffer)
            if colored.strip():
                self.output_queue.put(('output', colored))
            self.buffer = ''
    def flush(self):
        if self.buffer:
            colored = ansi_to_kivy_markup(self.buffer)
            if colored.strip():
                self.output_queue.put(('output', colored))
            self.buffer = ''


class InputRedirector:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.closed = False
    def _get_input(self, prompt=''):
        if prompt:
            colored = ansi_to_kivy_markup(prompt)
            self.output_queue.put(('output', colored))
        self.output_queue.put(('need_input', True))
        result = self.input_queue.get()
        return result
    def __call__(self, prompt=''):
        return self._get_input(prompt)
    def readline(self, size=-1):
        return self._get_input() + '\n'
    def read(self, size=-1):
        return self._get_input()
    def readlines(self, hint=-1):
        return [self._get_input() + '\n']
    def isatty(self):
        return False
    def flush(self):
        pass
    def close(self):
        self.closed = True
    def __iter__(self):
        return self
    def __next__(self):
        return self.readline()


class OsSystemRedirector:
    def __init__(self, output_queue):
        self.output_queue = output_queue
        self._original = os.system
    def __call__(self, cmd):
        cmd_lower = str(cmd).lower()
        if 'cls' in cmd_lower or 'clear' in cmd_lower:
            self.output_queue.put(('clear', True))
            return 0
        return self._original(cmd)


class FuncButton(Button):
    def __init__(self, name, command, app=None, **kwargs):
        super().__init__(**kwargs)
        self.text = name
        self.command = command
        self.app = app
        self.size_hint_y = None
        self.height = 42
        self.font_size = '12sp'
        self.background_normal = ''
        self.background_color = (0.15, 0.35, 0.55, 1)
        self.color = (1, 1, 1, 1)
        self.bind(on_press=self._on_press)
    def _on_press(self, instance):
        if self.app and hasattr(self.app, 'send_command'):
            self.app.send_command(self.command)


class PVZ2GUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        self.script_thread = None
        self.waiting_for_input = False
        self.padding = 4
        self.spacing = 3
        self._build_ui()
        Clock.schedule_interval(self._update_output, 0.1)

    def _build_ui(self):
        title = Label(
            text='[b]PVZ2 脚本工具 v3.5[/b]',
            size_hint=(1, 0.05),
            font_size='17sp',
            markup=True,
            color=(0.9, 0.9, 1, 1)
        )
        self.add_widget(title)

        ctrl_layout = BoxLayout(size_hint=(1, 0.055), spacing=5)
        self.start_btn = Button(text='▶ 启动', on_press=self._start_script,
            background_normal='', background_color=(0.2, 0.6, 0.3, 1), font_size='13sp')
        self.clear_btn = Button(text='🗑 清屏', on_press=self._clear_output,
            background_normal='', background_color=(0.5, 0.5, 0.5, 1), font_size='13sp')
        self.stop_btn = Button(text='⏹ 停止', on_press=self._stop_script, disabled=True,
            background_normal='', background_color=(0.7, 0.2, 0.2, 1), font_size='13sp')
        ctrl_layout.add_widget(self.start_btn)
        ctrl_layout.add_widget(self.clear_btn)
        ctrl_layout.add_widget(self.stop_btn)
        self.add_widget(ctrl_layout)

        self.tab_panel = TabbedPanel(
            size_hint=(1, 0.42),
            do_default_tab=False,
            tab_width=70,
            background_color=(0.1, 0.1, 0.12, 1)
        )
        cat_order = ["登录", "常用", "日常", "追击", "无尽", "转基因", "双人", "回忆", "秘境",
                      "限时", "响叮当", "一次性", "庭院", "聚宝盆", "砸罐", "同游",
                      "家族", "存档", "令营", "晚会", "僵局"]
        for cat_name in cat_order:
            if cat_name not in CATEGORIES:
                continue
            tab = TabbedPanelItem(text=cat_name, font_size='11sp')
            scroll = ScrollView()
            grid = GridLayout(cols=3, spacing=3, padding=3, size_hint_y=None)
            grid.bind(minimum_height=grid.setter('height'))
            for func_name, cmd in CATEGORIES[cat_name]:
                btn = FuncButton(name=func_name, command=cmd, app=self)
                grid.add_widget(btn)
            scroll.add_widget(grid)
            tab.add_widget(scroll)
            self.tab_panel.add_widget(tab)
        self.add_widget(self.tab_panel)

        output_label = Label(
            text='[color=888888]输出日志：[/color]',
            size_hint=(1, 0.025),
            font_size='10sp',
            markup=True,
            halign='left'
        )
        output_label.bind(size=lambda i, v: setattr(i, 'text_size', v))
        self.add_widget(output_label)

        output_container = BoxLayout(size_hint=(1, 0.35))
        self.output_view = ScrollView(bar_width=6)
        self.output_label = Label(
            text='[color=666666]点击"启动"运行脚本\n点击上方功能按钮直接执行[/color]\n',
            size_hint_y=None,
            font_size='10sp',
            text_size=(Window.width - 20, None),
            valign='top',
            markup=True
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.output_view.add_widget(self.output_label)
        output_container.add_widget(self.output_view)
        self.add_widget(output_container)

        input_layout = BoxLayout(size_hint=(1, 0.05), spacing=5, padding=(0, 3, 0, 0))
        self.input_field = TextInput(
            hint_text='手动输入...',
            multiline=False,
            disabled=True,
            font_size='11sp',
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0.9, 0.9, 0.9, 1)
        )
        self.input_btn = Button(
            text='发送', size_hint=(0.15, 1), on_press=self._send_input,
            disabled=True, background_normal='', background_color=(0.2, 0.5, 0.8, 1), font_size='12sp'
        )
        input_layout.add_widget(self.input_field)
        input_layout.add_widget(self.input_btn)
        self.add_widget(input_layout)

        Window.bind(on_resize=self._on_window_resize)

    def _on_window_resize(self, instance, width, height):
        self.output_label.text_size = (width - 20, None)

    def send_command(self, command):
        if not self.waiting_for_input:
            self._append_output('[color=ffaa00]请先启动脚本并等待输入提示[/color]\n')
            return
        lines = command.split('\n')
        for i, line in enumerate(lines):
            self.input_queue.put(line)
            if i < len(lines) - 1:
                self._append_output(f'[color=88ccff]> {line}[/color]\n')
        self.input_field.text = ''
        self.input_field.disabled = True
        self.input_btn.disabled = True
        self.waiting_for_input = False

    def _start_script(self, instance):
        if self.script_thread and self.script_thread.is_alive():
            return
        self.output_label.text = ''
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.script_thread = threading.Thread(target=self._run_script, daemon=True)
        self.script_thread.start()

    def _stop_script(self, instance):
        if self.script_thread:
            self._append_output('\n[color=ff6666][用户停止][/color]\n')
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            self.input_field.disabled = True
            self.input_btn.disabled = True

    def _clear_output(self, instance):
        self.output_label.text = ''

    def _run_script(self):
        try:
            with open(SCRIPT_PATH, 'r', encoding='utf-8-sig') as f:
                script_code = f.read()
            old_stdout = sys.stdout
            old_stdin = sys.stdin
            old_os_system = os.system
            sys.stdout = OutputRedirector(self.output_queue)
            sys.stdin = InputRedirector(self.input_queue, self.output_queue)
            os.system = OsSystemRedirector(self.output_queue)
            exec(script_code, {'__name__': '__main__'})
            sys.stdout = old_stdout
            sys.stdin = old_stdin
            os.system = old_os_system
            self.output_queue.put(('finished', True))
        except Exception as e:
            import traceback
            self.output_queue.put(('output', f'\n[color=ff4444][出错] {e}[/color]\n{traceback.format_exc()}\n'))
            self.output_queue.put(('finished', True))

    def _send_input(self, instance):
        text = self.input_field.text
        self.input_queue.put(text)
        self._append_output(f'[color=88ccff]> {text}[/color]\n')
        self.input_field.text = ''
        self.input_field.disabled = True
        self.input_btn.disabled = True
        self.waiting_for_input = False

    def _update_output(self, dt):
        try:
            while True:
                msg_type, msg = self.output_queue.get_nowait()
                if msg_type == 'output':
                    self._append_output(msg)
                elif msg_type == 'need_input':
                    self.waiting_for_input = True
                    self.input_field.disabled = False
                    self.input_btn.disabled = False
                    self.input_field.focus = True
                elif msg_type == 'clear':
                    self.output_label.text = ''
                elif msg_type == 'finished':
                    self.start_btn.disabled = False
                    self.stop_btn.disabled = True
                    self.input_field.disabled = True
                    self.input_btn.disabled = True
        except queue.Empty:
            pass

    def _append_output(self, text):
        self.output_label.text += text
        if len(self.output_label.text) > 100000:
            self.output_label.text = self.output_label.text[-60000:]
        Clock.schedule_once(lambda dt: setattr(self.output_view, 'scroll_y', 0), 0.01)


class PVZ2App(App):
    def build(self):
        self.title = 'PVZ2 脚本工具'
        Window.clearcolor = (0.08, 0.08, 0.1, 1)
        return PVZ2GUI()


if __name__ == '__main__':
    PVZ2App().run()
