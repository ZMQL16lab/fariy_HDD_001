import tkinter as tk
import random
import time
import threading
import pygame
import os
from tkinter import font as tkfont
from PIL import Image, ImageTk

# ----- 启动窗口类 -----
class BootScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Fairy 启动中")
        self.root.geometry("600x400")
        self.root.configure(bg="#0a0a1a")
        self.root.resizable(False, False)

        self.title_font = tkfont.Font(family="Consolas", size=20, weight="bold")
        self.code_font = tkfont.Font(family="Consolas", size=10)

        # 跑码区域
        self.code_frame = tk.Frame(root, bg="#0a0a1a", height=200)
        self.code_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.code_text = tk.Text(
            self.code_frame,
            bg="#0a0a1a",
            fg="#00ffcc",
            font=self.code_font,
            wrap=tk.WORD,
            height=10,
            relief=tk.FLAT,
            highlightthickness=0,
            bd=0
        )
        self.code_text.pack(fill=tk.BOTH, expand=True)
        self.code_text.insert(tk.END, "╔══════════════════════════════════════════════════╗\n")
        self.code_text.insert(tk.END, "║  Ⅲ型総序式統合汎用人工知能システム起動中...    ║\n")
        self.code_text.insert(tk.END, "║  Ver 2.17.4  |  SYS: 全チェック完了             ║\n")
        self.code_text.insert(tk.END, "╚══════════════════════════════════════════════════╝\n")
        self.code_text.config(state=tk.DISABLED)

        self.progress_var = tk.StringVar()
        self.progress_var.set("起動準備中...")
        self.progress_label = tk.Label(
            root,
            textvariable=self.progress_var,
            bg="#0a0a1a",
            fg="#00ffcc",
            font=self.code_font
        )
        self.progress_label.pack(pady=5)

        self.go_btn = tk.Button(
            root,
            text="⚡ 启动 Fairy",
            command=self.start_animation,
            font=("Consolas", 12),
            bg="#0a0a1a",
            fg="#00ffcc",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2"
        )
        self.go_btn.pack(pady=10)

    # ----- 跑码动画 -----
    def start_animation(self):
        self.go_btn.config(state=tk.DISABLED)
        self.progress_var.set("コード解析中...")

        code_lines = [
            "[Fairy] セッションを初期化...",
            "[Fairy] 接続先: null",
            "[Fairy] プロトコル: 独自",
            "[Fairy] ハッシュ確認: OK",
            "[Fairy] トレース中...",
            "[Fairy] 要請: 信頼度 99.9%",
            "[Fairy] システムチェック完了。",
            "[Fairy] ——— ファイナライズ ———"
        ]

        def animate():
            self.progress_var.set("⚡ 起動シーケンス実行中...")
            for line in code_lines:
                time.sleep(random.uniform(0.3, 0.8))
                self.code_text.config(state=tk.NORMAL)
                self.code_text.insert(tk.END, f"\n{line}")
                self.code_text.see(tk.END)
                self.code_text.config(state=tk.DISABLED)

            self.progress_var.set("✅ 起動完了 – Fairy オープン")
            self.open_eye_window()

        threading.Thread(target=animate, daemon=True).start()

    # ----- Fairy 主窗口 -----
    def open_eye_window(self):
        eye_win = tk.Toplevel(self.root)
        eye_win.title("Fairy")
        eye_win.attributes("-fullscreen", True)
        eye_win.configure(bg="#000000")
        eye_win.bind("<Escape>", lambda e: [eye_win.destroy(), self.root.quit()])

        # 加载 GIF
        gif_path = "fairy.gif"
        try:
            img = Image.open(gif_path)
            frames = []
            try:
                while True:
                    frames.append(ImageTk.PhotoImage(img.copy()))
                    img.seek(len(frames))
            except EOFError:
                pass
        except Exception as e:
            print(f"⚠️ GIF 加载失败: {e}")
            return

        # 显示 GIF
        label = tk.Label(eye_win, bg="#0a0a1a")
        label.pack(expand=True)

        # 绑定左键点击
        label.bind("<Button-1>", self.on_click)

        # ---------- 音频初始化 ----------
        # 语音文件列表（放在 audio/ 目录下，命名 fairy_01.mp3 ~ fairy_10.mp3）
        self.audio_dir = "audio"
        self.audio_files = [f for f in os.listdir(self.audio_dir) if f.endswith(".mp3")]

        # 初始化 pygame mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # 播放启动语音
        try:
            pygame.mixer.music.load("Fariy_Start.mp3")
            pygame.mixer.music.play()
        except Exception as e:
            print(f"⚠️ 启动音频播放失败: {e}")

        # 空闲计时器相关
        self.idle_timer = None
        self.is_idle = True
        self.start_idle_timer()

        # 关闭按钮
        close_btn = tk.Button(
            eye_win,
            text="✖",
            command=lambda: [eye_win.destroy(), self.root.quit()],
            font=("Consolas", 16),
            bg="#0a0a1a",
            fg="#ff4466",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2"
        )
        close_btn.place(x=eye_win.winfo_screenwidth() - 60, y=20)

        # 保存引用
        self.eye_frames = frames
        self.eye_label = label
        self.eye_win = eye_win
        self._animate_gif(0)

        # 隐藏主窗口
        self.root.withdraw()

    # ----- GIF 循环动画 -----
    def _animate_gif(self, idx):
        if not hasattr(self, 'eye_frames') or not self.eye_frames:
            return
        try:
            self.eye_label.config(image=self.eye_frames[idx])
            self.eye_win.after(66, self._animate_gif, (idx + 1) % len(self.eye_frames))
        except:
            pass

    # ---------- 语音播放 ----------
    def play_random_audio(self):
        if not self.audio_files:
            return
        audio_file = random.choice(self.audio_files)
        audio_path = os.path.join(self.audio_dir, audio_file)
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"⚠️ 播放失败: {e}")

    # ---------- 交互事件 ----------
    def on_click(self, event):
        if not hasattr(self, 'audio_files') or not self.audio_files:
            return
        self.is_idle = False
        if self.idle_timer:
            self.root.after_cancel(self.idle_timer)
            self.idle_timer = None

        # 停止当前语音，播放新语音
        pygame.mixer.music.stop()
        self.play_random_audio()

        # 重置空闲计时器
        self.start_idle_timer()

    # ---------- 空闲计时器 ----------
    def start_idle_timer(self):
        self.is_idle = True
        # 5 分钟 = 300000 毫秒
        self.idle_timer = self.root.after(300000, self.on_idle)

    def on_idle(self):
        if self.is_idle:
            self.play_random_audio()
        # 循环计时
        self.start_idle_timer()

# ----- 程序入口 -----
if __name__ == "__main__":
    root = tk.Tk()
    app = BootScreen(root)
    root.mainloop()