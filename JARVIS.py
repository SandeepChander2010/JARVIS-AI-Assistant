"""
JARVISE BLACK EDITION — WAKE COMMAND REQUIRED (FIXED)
=====================================================
MUST say "Wake Up" FIRST before ANY command works!
With FULL CODING AI - 40+ Programming Languages + Spotify
"""

import sys
import os
import subprocess
import datetime
import webbrowser
import socket
import random

from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

# ── Optional deps ─────────────────────────────────────────────────────────────
try:    import pyttsx3;           TTS_AVAILABLE    = True
except: TTS_AVAILABLE    = False

try:    import psutil;            PSUTIL_AVAILABLE = True
except: PSUTIL_AVAILABLE = False

try:    import pyautogui;         AUTOGUI_AVAILABLE = True
except: AUTOGUI_AVAILABLE = False

try:    import pywhatkit as kit;  YT_AVAILABLE = True
except: YT_AVAILABLE = False

try:    from ollama import Client as OllamaClient; OLLAMA_AVAILABLE = True
except: OLLAMA_AVAILABLE = False


# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#080808"
PANEL    = "#111111"
CARD     = "#181818"
RED      = "#ff2222"
RED2     = "#ff6666"
RED3     = "#cc1111"
CYAN     = "#00ffcc"
YELLOW   = "#ffcc00"
ORANGE   = "#ff8800"
PURPLE   = "#bb44ff"
BLUE     = "#2288ff"
GREEN    = "#1DB954"
WHITE    = "#ffffff"
GREY     = "#bbbbbb"
DGREY    = "#555555"

F_TINY   = 11
F_SMALL  = 13
F_BASE   = 15
F_MED    = 17
F_LARGE  = 20
F_HUGE   = 38
F_TITLE  = 22

MONO = "'Courier New', 'Consolas', monospace"
SANS = "'Segoe UI', 'Arial', sans-serif"

STYLE = f"""
QMainWindow, QWidget {{ background: {BG}; color: {WHITE}; font-family: {SANS}; font-size: {F_BASE}px; }}
QTabWidget::pane {{ background: {BG}; border: 2px solid {RED}; border-radius: 8px; }}
QTabBar::tab {{ background: {CARD}; color: {GREY}; padding: 12px 28px; margin: 3px; border: 1px solid {RED3}; border-radius: 6px; font-size: {F_LARGE}px; font-weight: bold; min-width: 140px; }}
QTabBar::tab:selected {{ background: {RED}; color: {WHITE}; border: 1px solid {RED2}; }}
QTabBar::tab:hover:!selected {{ background: #280808; color: {RED2}; }}
QTextEdit, QPlainTextEdit {{ background: {CARD}; color: {CYAN}; border: 1px solid {RED3}; border-radius: 6px; padding: 12px; font-family: {MONO}; font-size: {F_BASE}px; }}
QLineEdit {{ background: {CARD}; color: {CYAN}; border: 1px solid {RED3}; border-radius: 6px; padding: 10px 16px; font-size: {F_BASE}px; }}
QComboBox {{ background: {CARD}; color: {CYAN}; border: 1px solid {RED3}; border-radius: 6px; padding: 8px 14px; font-size: {F_BASE}px; }}
QGroupBox {{ color: {RED2}; border: 1px solid {RED}; border-radius: 6px; margin-top: 16px; font-size: {F_MED}px; font-weight: bold; }}
QProgressBar {{ border: none; background: #1a1a1a; border-radius: 5px; height: 16px; }}
QProgressBar::chunk {{ background: {RED}; border-radius: 5px; }}
QScrollBar:vertical {{ background: {CARD}; width: 10px; border-radius: 5px; }}
QScrollBar::handle:vertical {{ background: {RED3}; border-radius: 5px; min-height: 40px; }}
QSplitter::handle {{ background: {RED3}; }}
QLabel {{ color: {WHITE}; }}
"""


def make_btn(text, bg, fg=WHITE, fs=F_MED, h=46):
    b = QPushButton(text)
    b.setMinimumHeight(h)
    b.setStyleSheet(f"""
        QPushButton {{ background: {bg}; color: {fg}; border: none; border-radius: 6px;
        padding: 8px 18px; font-size: {fs}px; font-weight: bold; }}
        QPushButton:hover {{ background: {bg}cc; border: 1px solid {WHITE}44; }}
        QPushButton:pressed {{ background: {bg}88; }}
    """)
    return b

def make_label(text, color=WHITE, fs=F_BASE, bold=False, align=Qt.AlignLeft):
    lbl = QLabel(text)
    lbl.setAlignment(align)
    w = "bold" if bold else "normal"
    lbl.setStyleSheet(f"color:{color}; font-size:{fs}px; font-weight:{w}; border:none;")
    return lbl

def glow_frame(border=RED, bg=PANEL, radius=8):
    f = QFrame()
    f.setStyleSheet(f"QFrame {{ background:{bg}; border:1px solid {border}; border-radius:{radius}px; }}")
    return f


class StatCard(QFrame):
    def __init__(self, title, color):
        super().__init__()
        self.setStyleSheet(f"QFrame {{ background:{PANEL}; border:2px solid {color}; border-radius:8px; padding:6px; }}")
        lay = QVBoxLayout(self); lay.setSpacing(6)
        t = QLabel(f"▣  {title}")
        t.setStyleSheet(f"color:{color}; font-size:{F_MED}px; font-weight:bold;")
        lay.addWidget(t)
        self.val = QLabel("--")
        self.val.setStyleSheet(f"color:{color}; font-size:{F_HUGE}px; font-weight:bold;")
        lay.addWidget(self.val)
        self.bar = QProgressBar()
        self.bar.setMaximum(100); self.bar.setTextVisible(False); self.bar.setFixedHeight(14)
        self.bar.setStyleSheet(f"QProgressBar {{ background:#111; border:none; border-radius:7px; }} QProgressBar::chunk {{ background:{color}; border-radius:7px; }}")
        lay.addWidget(self.bar)
        self.sub = QLabel("")
        self.sub.setStyleSheet(f"color:{color}99; font-size:{F_SMALL}px;")
        lay.addWidget(self.sub)

    def update(self, val_str, pct, sub=""):
        self.val.setText(val_str)
        self.bar.setValue(int(min(100, max(0, pct))))
        self.sub.setText(sub)


class YouTubeMusicPlayer(QThread):
    status_changed = pyqtSignal(str)
    now_playing = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.query = ""
        self.is_playing = False
    
    def play(self, song_or_url):
        self.query = song_or_url
        self.is_playing = True
        self.now_playing.emit(f"▶ Playing: {song_or_url[:50]}...")
        self.start()
    
    def run(self):
        if YT_AVAILABLE:
            try:
                kit.playonyt(self.query)
            except:
                webbrowser.open(f"https://youtube.com/results?search_query={self.query.replace(' ', '+')}")
        else:
            webbrowser.open(f"https://youtube.com/results?search_query={self.query.replace(' ', '+')}")
        self.is_playing = False
    
    def stop(self):
        self.is_playing = False
        self.now_playing.emit("⏹ Music stopped")


class OllamaBrain(QThread):
    response_ready = pyqtSignal(str)
    thinking       = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)

    CODING_MODELS = ["deepseek-coder:6.7b", "deepseek-coder", "codellama:13b", "codellama", "llama3.1:8b", "llama3.2"]
    CHAT_MODELS   = ["llama3.2", "llama3.1", "mistral"]

    def __init__(self):
        super().__init__()
        self.client = None
        self.model = "llama3.2"
        self.chat_model = "llama3.2"
        self._sys = ""
        self._user = ""
        self._hist = True
        self.history = []
        self._available_models = []
        self._connect()

    def _connect(self):
        if OLLAMA_AVAILABLE:
            try:
                self.client = OllamaClient(host='http://localhost:11434')
                raw = self.client.list()
                models = raw.get('models', []) if isinstance(raw, dict) else []
                self._available_models = [m['name'] for m in models if 'name' in m]
                for m in self.CODING_MODELS:
                    if any(m in am for am in self._available_models):
                        self.model = m
                        break
                else:
                    if self._available_models:
                        self.model = self._available_models[0]
                for m in self.CHAT_MODELS:
                    if any(m in am for am in self._available_models):
                        self.chat_model = m
                        break
                else:
                    self.chat_model = self.model
            except:
                self.client = None

    def get_available_models(self):
        return self._available_models if self._available_models else ["llama3.2", "codellama", "deepseek-coder"]

    def is_available(self):
        return self.client is not None

    def _send(self, system, user, use_history=True):
        if not self.is_available():
            self.error_occurred.emit("Ollama not connected. Run: ollama serve")
            return
        self._sys, self._user, self._hist = system, user, use_history
        self.thinking.emit(True)
        self.start()

    def chat(self, msg):
        self.model = self.chat_model
        self._send("You are JARVISE, a helpful AI assistant. Give clear, direct answers.", msg)

    def code_action(self, action, text, lang):
        prompts = {
            "generate": f"Write clean, working {lang} code for:\n{text}\nReturn ONLY the code with brief comments.",
            "explain": f"Explain this {lang} code step by step:\n```{lang.lower()}\n{text}\n```",
            "debug": f"Debug this {lang} code. Find bugs and provide corrected code:\n```{lang.lower()}\n{text}\n```",
            "optimize": f"Optimize this {lang} code for performance:\n```{lang.lower()}\n{text}\n```",
            "convert": f"Convert this code to {lang}:\n{text}",
            "review": f"Code review this {lang} code:\n```{lang.lower()}\n{text}\n```",
            "test": f"Write unit tests for this {lang} code:\n```{lang.lower()}\n{text}\n```",
            "document": f"Add documentation to this {lang} code:\n```{lang.lower()}\n{text}\n```",
        }
        self._send(f"You are an expert {lang} developer. Be precise and thorough.", prompts.get(action, text), use_history=False)

    def question(self, q):
        self.model = self.chat_model
        self._send("You are JARVISE, a highly intelligent AI. Give clear answers.", q)

    def run(self):
        try:
            msgs = [{"role": "system", "content": self._sys}]
            if self._hist:
                msgs += self.history[-16:]
            msgs.append({"role": "user", "content": self._user})
            is_code = not self._hist
            opts = {
                "temperature": 0.2 if is_code else 0.7,
                "num_predict": 4096 if is_code else 2048,
                "top_p": 0.9,
            }
            resp = self.client.chat(model=self.model, messages=msgs, options=opts)
            answer = resp['message']['content'].strip()
            if self._hist:
                self.history += [
                    {"role": "user", "content": self._user[:400]},
                    {"role": "assistant", "content": answer[:400]},
                ]
                if len(self.history) > 30:
                    self.history = self.history[-30:]
            self.response_ready.emit(answer)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.thinking.emit(False)

    def clear_history(self):
        self.history = []


class VoiceEngine:
    def __init__(self):
        self.engine = None
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 175)
                self.engine.setProperty('volume', 0.9)
            except:
                pass

    def speak(self, text):
        if self.engine:
            try:
                self.engine.say(str(text)[:400].replace('\n', ' '))
                self.engine.runAndWait()
            except:
                pass


# ── WAKE MANAGER - MUST SAY WAKE UP FIRST ─────────────────────────────────────
class WakeManager:
    def __init__(self):
        self.is_awake = False
        self.wake_word = "wake up"
    
    def check_wake_word(self, text):
        if text and self.wake_word in text.lower():
            self.is_awake = True
            return True
        return False
    
    def is_awake_status(self):
        return self.is_awake
    
    def wake(self):
        self.is_awake = True
    
    def sleep(self):
        self.is_awake = False


class VoiceWorker(QThread):
    got_command = pyqtSignal(str)
    status_msg  = pyqtSignal(str)
    wake_heard  = pyqtSignal()

    def __init__(self, wake_manager):
        super().__init__()
        self.wake_manager = wake_manager
        self.running = True
        self.rec = self.mic = None
        try:
            import speech_recognition as sr
            self.rec = sr.Recognizer()
            self.mic = sr.Microphone()
        except:
            pass

    def run(self):
        if not self.rec:
            return
        while self.running:
            try:
                with self.mic as source:
                    if not self.wake_manager.is_awake_status():
                        self.status_msg.emit("🔴 Say 'Wake Up' first...")
                    else:
                        self.status_msg.emit("🟢 Awake! Say command...")
                    
                    self.rec.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.rec.listen(source, timeout=2, phrase_time_limit=3)
                    text = self.rec.recognize_google(audio, language='en-IN')
                    
                    if self.wake_manager.check_wake_word(text):
                        self.wake_heard.emit()
                        self.status_msg.emit("🟢 Awake! Say your command...")
                        audio = self.rec.listen(source, timeout=8, phrase_time_limit=8)
                        cmd = self.rec.recognize_google(audio, language='en-IN')
                        if cmd:
                            self.got_command.emit(cmd)
                        self.status_msg.emit("🟢 Ready for next command...")
                    elif self.wake_manager.is_awake_status():
                        self.got_command.emit(text)
            except Exception as e:
                continue

    def stop(self):
        self.running = False


# ─────────────────────────────────────────────────────────────────────────────
# MAIN WINDOW
# ─────────────────────────────────────────────────────────────────────────────
class Jarvise(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ai = OllamaBrain()
        self.wm = WakeManager()
        self.voice = VoiceEngine()
        self.youtube = YouTubeMusicPlayer()
        self.vw = None
        self._target = "chat"

        self.ai.response_ready.connect(self._ai_response)
        self.ai.thinking.connect(self._ai_thinking)
        self.ai.error_occurred.connect(self._ai_error)
        self.youtube.now_playing.connect(self._update_now_playing)

        try:
            self.vw = VoiceWorker(self.wm)
            self.vw.got_command.connect(self._voice_cmd)
            self.vw.status_msg.connect(self._voice_status)
            self.vw.wake_heard.connect(self._on_wake_detected)
            self.vw.start()
        except:
            pass

        self._build()
        self._sys_timer = QTimer()
        self._sys_timer.timeout.connect(self._update_sys)
        self._sys_timer.start(3000)
        self._update_sys()
        QTimer.singleShot(500, self._welcome)

    def _build(self):
        self.setWindowTitle("⚡ JARVISE - Coding AI + Q/A AI ⚡")
        self.setMinimumSize(1400, 850)
        self.setStyleSheet(STYLE)
        root = QWidget()
        self.setCentralWidget(root)
        lay = QVBoxLayout(root)
        lay.setContentsMargins(14, 10, 14, 8)
        lay.setSpacing(8)
        lay.addWidget(self._header())
        lay.addWidget(self._tabs(), 1)
        lay.addWidget(self._footer())

    def _header(self):
        f = glow_frame(RED)
        lay = QHBoxLayout(f)
        lay.setContentsMargins(16, 10, 16, 10)
        lay.setSpacing(14)

        left = QVBoxLayout()
        left.setSpacing(4)
        left.addWidget(make_label("⚡  JARVISE - Coding AI + Q/A AI ⚡", RED2, F_TITLE, bold=True))
        left.addWidget(make_label("⚠️ MUST SAY 'WAKE UP' FIRST before any command! | 40+ Programming Languages | Q/A", YELLOW, F_SMALL))
        lay.addLayout(left)
        lay.addStretch()

        right = glow_frame(RED3, CARD)
        rl = QHBoxLayout(right)
        rl.setContentsMargins(12, 8, 12, 8)
        rl.setSpacing(12)

        self.awake_lbl = make_label("🔴 SLEEPING", RED2, F_MED, bold=True)
        rl.addWidget(self.awake_lbl)

        self.voice_status = make_label("🎤 Say 'Wake Up'...", CYAN, F_SMALL)
        rl.addWidget(self.voice_status)

        wake_btn = make_btn("⚡ Wake Up", CYAN, "#000", F_MED, 42)
        wake_btn.setFixedWidth(130)
        wake_btn.clicked.connect(self._manual_wake)
        rl.addWidget(wake_btn)

        sleep_btn = make_btn("😴 Sleep", RED2, WHITE, F_MED, 42)
        sleep_btn.setFixedWidth(100)
        sleep_btn.clicked.connect(self._manual_sleep)
        rl.addWidget(sleep_btn)

        exit_btn = make_btn("✕ Exit", RED, WHITE, F_MED, 42)
        exit_btn.setFixedWidth(90)
        exit_btn.clicked.connect(self.close)
        rl.addWidget(exit_btn)

        lay.addWidget(right)
        return f

    def _tab_music(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)

        title = make_label("🎵 YOUTUBE MUSIC PLAYER", YELLOW, F_LARGE, bold=True, align=Qt.AlignCenter)
        title.setStyleSheet(f"background:{CARD}; border-radius:10px; padding:15px;")
        layout.addWidget(title)

        search_frame = glow_frame(CYAN)
        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(15, 10, 15, 10)

        self.music_input = QLineEdit()
        self.music_input.setPlaceholderText("Enter song name, artist, or YouTube URL...")
        self.music_input.setMinimumHeight(50)
        search_layout.addWidget(self.music_input)

        play_btn = make_btn("▶ PLAY", CYAN, "#000", F_MED, 50)
        play_btn.setFixedWidth(120)
        play_btn.clicked.connect(self._play_youtube)
        search_layout.addWidget(play_btn)

        layout.addWidget(search_frame)

        quick_label = make_label("🔥 POPULAR SONGS", YELLOW, F_MED, bold=True, align=Qt.AlignCenter)
        layout.addWidget(quick_label)

        quick_frame1 = glow_frame(RED3)
        quick_layout1 = QHBoxLayout(quick_frame1)
        quick_layout1.setSpacing(10)

        popular_songs = [
            ("🎤 Shape of You", "Shape of You"),
            ("🎸 Beat It", "Beat It"),
            ("🎹 Blinding Lights", "Blinding Lights"),
            ("🎧 Billie Jean", "Billie Jean"),
        ]
        for name, song in popular_songs:
            btn = make_btn(name, CARD, CYAN, F_SMALL, 40)
            btn.clicked.connect(lambda _, s=song: self._play_quick(s))
            quick_layout1.addWidget(btn)

        layout.addWidget(quick_frame1)

        self.now_playing_label = make_label("🎵 Ready to play music", CYAN, F_MED, bold=True, align=Qt.AlignCenter)
        self.now_playing_label.setStyleSheet(f"background:{CARD}; padding:15px; border-radius:8px;")
        layout.addWidget(self.now_playing_label)

        control_frame = glow_frame(RED2)
        control_layout = QHBoxLayout(control_frame)
        stop_btn = make_btn("⏹ STOP", RED2, WHITE, F_MED, 50)
        stop_btn.clicked.connect(self._stop_music)
        control_layout.addWidget(stop_btn)
        control_layout.addStretch()
        layout.addWidget(control_frame)
        layout.addStretch()
        return tab

    def _play_youtube(self):
        if not self.wm.is_awake_status():
            self._add_chat("⚠️ I'm sleeping! Please say 'Wake Up' first.", "jarvis")
            self.voice.speak("Please wake me up first.")
            return
        query = self.music_input.text().strip()
        if query:
            self.youtube.play(query)
            self._add_chat(f"🎵 Playing: {query[:50]}", "jarvis")

    def _play_quick(self, query):
        if not self.wm.is_awake_status():
            self._add_chat("⚠️ I'm sleeping! Please say 'Wake Up' first.", "jarvis")
            self.voice.speak("Please wake me up first.")
            return
        self.music_input.setText(query)
        self._play_youtube()

    def _stop_music(self):
        self.youtube.stop()
        self.now_playing_label.setText("🎵 Music stopped")
        self._add_chat("🎵 Music stopped", "jarvis")

    def _update_now_playing(self, message):
        self.now_playing_label.setText(message)

    # ── CODING AI TAB ───────────────────────────────────────────────────────────
    def _tab_code_ai(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(8)

        # Toolbar with Language Selector
        tb = glow_frame(RED3, CARD)
        tl = QHBoxLayout(tb)
        tl.setContentsMargins(12, 8, 12, 8)
        tl.setSpacing(14)
        
        tl.addWidget(make_label("Language:", CYAN, F_BASE))
        self.code_lang = QComboBox()
        all_languages = [
            "Python", "JavaScript", "TypeScript", "Java", "C", "C++", "C#",
            "Go", "Rust", "Swift", "Kotlin", "PHP", "Ruby", "Perl",
            "R", "MATLAB", "Scala", "Dart", "Lua", "Bash/Shell",
            "PowerShell", "SQL", "HTML", "CSS", "SCSS", "Sass",
            "React/JSX", "Vue", "Angular", "Svelte", "Solidity",
            "Assembly", "Haskell", "Erlang", "Elixir", "F#",
            "Clojure", "Groovy", "Julia", "OCaml", "Scheme",
            "COBOL", "Fortran", "Pascal", "Delphi", "Ada",
            "Verilog", "VHDL", "SystemVerilog", "VBA", "Objective-C"
        ]
        self.code_lang.addItems(sorted(all_languages))
        self.code_lang.setFixedWidth(180)
        tl.addWidget(self.code_lang)
        
        tl.addStretch()
        
        tl.addWidget(make_label("AI Model:", CYAN, F_BASE))
        self.code_model = QComboBox()
        code_models = self.ai.get_available_models() or ["llama3.2", "codellama", "deepseek-coder"]
        self.code_model.addItems(code_models)
        idx = self.code_model.findText(self.ai.model)
        if idx >= 0:
            self.code_model.setCurrentIndex(idx)
        self.code_model.setFixedWidth(200)
        tl.addWidget(self.code_model)
        
        layout.addWidget(tb)

        # Action Buttons
        af = glow_frame(RED3, CARD)
        al = QHBoxLayout(af)
        al.setContentsMargins(10, 8, 10, 8)
        al.setSpacing(8)
        
        action_buttons = [
            ("✨ Generate", CYAN, "#000", "generate"),
            ("📖 Explain", YELLOW, "#000", "explain"),
            ("🐛 Debug", RED2, WHITE, "debug"),
            ("⚡ Optimize", ORANGE, WHITE, "optimize"),
            ("🔄 Convert", PURPLE, WHITE, "convert"),
            ("🔍 Review", BLUE, WHITE, "review"),
            ("🧪 Tests", GREEN, WHITE, "test"),
            ("📚 Document", GREY, "#000", "document"),
        ]
        
        for label_txt, bg, fg, action in action_buttons:
            btn = make_btn(label_txt, bg, fg, F_MED, 46)
            btn.clicked.connect(lambda _, a=action: self._code_action(a))
            al.addWidget(btn)
        
        layout.addWidget(af)

        # Splitter for Input/Output
        spl = QSplitter(Qt.Horizontal)

        # Input Section
        left = QFrame()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 4, 0)
        ll.setSpacing(6)
        ll.addWidget(make_label("📝  INPUT — Paste code or describe what you want:", RED2, F_BASE, bold=True))
        
        self.code_input = QPlainTextEdit()
        self.code_input.setStyleSheet(f"""
            QPlainTextEdit {{
                background:{BG}; color:{WHITE}; border:1px solid {RED3};
                border-radius:6px; padding:14px;
                font-family:{MONO}; font-size:{F_BASE}px; line-height:1.6;
            }}
            QPlainTextEdit:focus {{ border:2px solid {RED}; }}
        """)
        self.code_input.setPlaceholderText(
            "Examples:\n"
            "• Write a REST API with JWT authentication\n"
            "• Write a Python function to sort a list\n"
            "• Create a binary search tree\n"
            "• Build a web scraper\n"
            "• [Paste your code here to explain/debug/optimize]"
        )
        ll.addWidget(self.code_input, 1)
        
        ex_row = QHBoxLayout()
        ex_row.setSpacing(6)
        examples = [
            ("Sort Algo", "Write an efficient sorting algorithm"),
            ("REST API", "Create a REST API with CRUD operations"),
            ("ML Model", "Write a simple machine learning classifier"),
            ("Web Scraper", "Build a web scraper"),
            ("CLI Tool", "Create a command-line tool"),
        ]
        for name, prompt in examples:
            eb = QPushButton(name)
            eb.setStyleSheet(f"""
                QPushButton {{
                    background:{CARD}; color:{GREY}; border:1px solid {RED3};
                    border-radius:4px; padding:6px 12px; font-size:{F_TINY}px;
                }}
                QPushButton:hover {{ color:{RED2}; border-color:{RED2}; }}
            """)
            eb.clicked.connect(lambda _, p=prompt: self.code_input.setPlainText(p))
            ex_row.addWidget(eb)
        ll.addLayout(ex_row)
        
        spl.addWidget(left)

        # Output Section
        right = QFrame()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(4, 0, 0, 0)
        rl.setSpacing(6)
        
        oh = QHBoxLayout()
        oh.addWidget(make_label("🤖  AI RESPONSE:", CYAN, F_BASE, bold=True))
        oh.addStretch()
        
        cp_btn = make_btn("📋 Copy", CARD, CYAN, F_SMALL, 34)
        cp_btn.setFixedWidth(100)
        cp_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.code_output.toPlainText()))
        oh.addWidget(cp_btn)
        
        clear_btn = make_btn("🗑 Clear", CARD, RED2, F_SMALL, 34)
        clear_btn.setFixedWidth(80)
        clear_btn.clicked.connect(lambda: self.code_output.clear())
        oh.addWidget(clear_btn)
        
        rl.addLayout(oh)

        self.code_output = QPlainTextEdit()
        self.code_output.setReadOnly(True)
        self.code_output.setStyleSheet(f"""
            QPlainTextEdit {{
                background:{BG}; color:{CYAN}; border:1px solid {RED3};
                border-radius:6px; padding:14px;
                font-family:{MONO}; font-size:{F_BASE}px; line-height:1.6;
            }}
        """)
        self.code_output.setPlaceholderText("AI generated code / explanation will appear here...")
        rl.addWidget(self.code_output, 1)
        
        spl.addWidget(right)
        spl.setSizes([550, 650])
        layout.addWidget(spl, 1)

        self.code_status = make_label("Ready — Choose language, paste code or describe what to build, then click an action.", GREY, F_SMALL)
        self.code_status.setStyleSheet(f"color:{GREY}; font-size:{F_SMALL}px; background:{CARD}; border-radius:4px; padding:6px;")
        layout.addWidget(self.code_status)
        
        return tab

    def _code_action(self, action):
        if not self.wm.is_awake_status():
            self.code_output.setPlainText("⚠️ I'm sleeping! Please say 'Wake Up' first.")
            return
            
        if not self.ai.is_available():
            self.code_output.setPlainText("❌ Ollama not connected.\n\nRun in terminal:\n  ollama serve\n\nThen restart JARVISE.")
            return
            
        text = self.code_input.toPlainText().strip()
        if not text:
            self.code_output.setPlainText("⚠️  Please enter code or a description first.")
            return
            
        lang = self.code_lang.currentText()
        self.ai.model = self.code_model.currentText()
        self._target = "code"
        self.code_status.setText(f"⏳  {action.capitalize()}ing {lang} code with {self.ai.model}...")
        self.code_output.setPlainText(f"🤔  JARVISE is {action}ing your {lang} code...\n\nPlease wait...")
        self.ai.code_action(action, text, lang)

    def _tabs(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(self._tab_actions(), "⚡ QUICK ACTION")
        self.tabs.addTab(self._tab_status(), "▣ SYSTEM STATUS")
        self.tabs.addTab(self._tab_music(), "🎵 MUSIC")
        self.tabs.addTab(self._tab_chat(), "▶ CHAT")
        self.tabs.addTab(self._tab_code_ai(), "⌨ CODING AI")
        self.tabs.addTab(self._tab_question(), "? QUESTION AI")
        return self.tabs

    # ── QUICK ACTIONS TAB (VOICE CONTROL SECTION REMOVED) ──────────────────────
    def _tab_actions(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(12)

        lay.addWidget(make_label("⚡  QUICK COMMANDS & ACTIONS", YELLOW, F_LARGE, bold=True, align=Qt.AlignCenter))
        
        notice = make_label("⚠️ FIRST: Click 'Wake Up' button or say 'Wake Up' before using commands!", ORANGE, F_SMALL, bold=True, align=Qt.AlignCenter)
        notice.setStyleSheet(f"background:{CARD}; border-radius:6px; padding:8px;")
        lay.addWidget(notice)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border:none;")
        inner = QWidget()
        il = QVBoxLayout(inner)
        il.setSpacing(14)

        # APPLICATIONS SECTION
        ag = QGroupBox("■  APPLICATIONS")
        ag_l = QGridLayout(ag)
        ag_l.setSpacing(8)
        apps = [
            ("🌐 Google Chrome", "chrome"),
            ("▶ YouTube", "youtube"),
            ("🎵 Spotify", "spotify"),
            ("🧮 Calculator", "calc"),
            ("📝 Notepad", "notepad"),
            ("💻 VS Code", "vscode"),
            ("📁 File Explorer", "explorer"),
        ]
        for i, (name, cmd) in enumerate(apps):
            btn = make_btn(name, RED2, WHITE, F_MED, 52)
            btn.clicked.connect(lambda _, c=cmd: self._syscmd(c))
            ag_l.addWidget(btn, i // 2, i % 2)
        il.addWidget(ag)

        # SYSTEM SECTION
        sg = QGroupBox("■  SYSTEM")
        sg_l = QGridLayout(sg)
        sg_l.setSpacing(8)
        system = [
            ("🔒 Lock PC", "lock"),
            ("💤 Sleep PC", "sleep"),
            ("🔄 Restart", "restart"),
            ("⏻ Shutdown", "shutdown"),
        ]
        for i, (name, cmd) in enumerate(system):
            btn = make_btn(name, RED2, WHITE, F_MED, 52)
            btn.clicked.connect(lambda _, c=cmd: self._syscmd(c))
            sg_l.addWidget(btn, i // 2, i % 2)
        il.addWidget(sg)

        # INFO SECTION
        ig = QGroupBox("ℹ  INFO")
        ig_l = QGridLayout(ig)
        ig_l.setSpacing(8)
        info = [
            ("🕐 Time", "time"),
            ("📅 Date", "date"),
            ("🔋 Battery", "battery"),
            ("💻 CPU", "cpu"),
        ]
        for i, (name, cmd) in enumerate(info):
            btn = make_btn(name, CYAN, "#000", F_MED, 52)
            btn.clicked.connect(lambda _, c=cmd: self._show_info(c))
            ig_l.addWidget(btn, i // 2, i % 2)
        il.addWidget(ig)

        il.addStretch()
        scroll.setWidget(inner)
        lay.addWidget(scroll)
        return tab

    def _tab_status(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(12)

        t = make_label("▣  SYSTEM PERFORMANCE MONITOR", WHITE, F_LARGE, bold=True, align=Qt.AlignCenter)
        t.setStyleSheet(f"background:{CARD}; border:1px solid {RED3}; padding:8px; border-radius:6px;")
        lay.addWidget(t)

        r1 = QHBoxLayout()
        r1.setSpacing(10)
        self.cpu_card = StatCard("CPU", RED2)
        self.ram_card = StatCard("RAM", CYAN)
        self.bat_card = StatCard("BATTERY", YELLOW)
        r1.addWidget(self.cpu_card)
        r1.addWidget(self.ram_card)
        r1.addWidget(self.bat_card)
        lay.addLayout(r1)

        ai_f = glow_frame(CYAN)
        al = QHBoxLayout(ai_f)
        self.ai_status_lbl = make_label("🤖  Checking Ollama...", CYAN, F_MED)
        al.addWidget(self.ai_status_lbl)
        al.addStretch()
        self.ai_model_lbl = make_label(f"Model: {self.ai.model}", GREY, F_SMALL)
        al.addWidget(self.ai_model_lbl)
        lay.addWidget(ai_f)
        lay.addStretch()
        return tab

    def _tab_chat(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(8)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet(f"background:{BG}; color:{CYAN}; border:1px solid {RED3}; border-radius:6px; padding:14px; font-family:{MONO};")
        lay.addWidget(self.chat_area, 1)

        bar = glow_frame(RED3, CARD)
        bl = QHBoxLayout(bar)
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type 'wake up' to activate, then type commands... (type 'help' for commands)")
        self.chat_input.returnPressed.connect(self._chat_send)
        bl.addWidget(self.chat_input, 1)

        s = make_btn("▶ Send", CYAN, "#000", F_MED, 46)
        s.clicked.connect(self._chat_send)
        c = make_btn("🗑 Clear", RED3, WHITE, F_MED, 46)
        c.clicked.connect(self._clear_chat)
        bl.addWidget(s)
        bl.addWidget(c)
        lay.addWidget(bar)
        return tab

    def _tab_question(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setSpacing(8)

        t = make_label("?  QUESTION AI", YELLOW, F_LARGE, bold=True, align=Qt.AlignCenter)
        t.setStyleSheet(f"background:{CARD}; border:1px solid {YELLOW}44; border-radius:6px; padding:8px;")
        lay.addWidget(t)

        qh = QHBoxLayout()
        qh.addWidget(make_label("Your Question:", YELLOW, F_BASE, bold=True))
        qh.addStretch()
        ask = make_btn("🚀 Ask AI", YELLOW, "#000", F_MED, 44)
        ask.clicked.connect(self._ask_q)
        qh.addWidget(ask)
        lay.addLayout(qh)

        self.q_input = QTextEdit()
        self.q_input.setMaximumHeight(150)
        self.q_input.setPlaceholderText("Ask any question...")
        lay.addWidget(self.q_input)

        self.q_output = QTextEdit()
        self.q_output.setReadOnly(True)
        self.q_output.setPlaceholderText("AI answer will appear here...")
        lay.addWidget(self.q_output)

        ch = make_btn("Clear History", CARD, GREY, F_SMALL, 34)
        ch.clicked.connect(lambda: (self.ai.clear_history(), self._add_chat("History cleared", "system")))
        lay.addWidget(ch)
        return tab

    def _footer(self):
        f = glow_frame(RED3, CARD, 5)
        lay = QHBoxLayout(f)
        self.footer_lbl = make_label("🔴 NOT ACTIVATED - Say 'WAKE UP' or type 'wake up' to start! | 40+ Languages |", YELLOW, F_TINY, bold=True)
        lay.addWidget(self.footer_lbl)
        return f

    def _syscmd(self, cmd):
        if not self.wm.is_awake_status():
            self._add_chat("⚠️ I'm sleeping! Please say 'Wake Up' or type 'wake up' first.", "jarvis")
            self.voice.speak("Please wake me up first. Say Wake Up.")
            return
        
        cmds = {
            "chrome": lambda: subprocess.Popen(["start", "chrome"], shell=True),
            "youtube": lambda: webbrowser.open("https://youtube.com"),
            "spotify": lambda: self._open_spotify(),
            "calc": lambda: subprocess.Popen("calc.exe"),
            "notepad": lambda: subprocess.Popen("notepad.exe"),
            "vscode": lambda: subprocess.Popen(["code"], shell=True),
            "explorer": lambda: subprocess.Popen("explorer.exe"),
            "music": lambda: self.tabs.setCurrentIndex(2),
            "stop": lambda: self._stop_music(),
            "vol_up": lambda: pyautogui.press('volumeup', presses=5) if AUTOGUI_AVAILABLE else None,
            "vol_down": lambda: pyautogui.press('volumedown', presses=5) if AUTOGUI_AVAILABLE else None,
            "lock": lambda: os.system("rundll32.exe user32.dll,LockWorkStation"),
            "sleep": lambda: QTimer.singleShot(2000, lambda: os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")),
            "restart": lambda: os.system("shutdown /r /t 5"),
            "shutdown": lambda: self._confirm_shutdown(),
        }
        if cmd in cmds:
            cmds[cmd]()
            self._add_chat(f"Executing: {cmd}", "jarvis")
            self.voice.speak(f"Executing {cmd}")

    def _open_spotify(self):
        try:
            spotify_paths = [
                r"C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe",
                r"C:\Program Files\Spotify\Spotify.exe",
                r"C:\Program Files (x86)\Spotify\Spotify.exe",
                "Spotify.exe"
            ]
            
            import os as os_module
            for path in spotify_paths:
                expanded_path = os_module.path.expandvars(path)
                if os_module.path.exists(expanded_path):
                    subprocess.Popen([expanded_path])
                    return
            
            webbrowser.open("https://open.spotify.com")
        except:
            webbrowser.open("https://open.spotify.com")

    def _confirm_shutdown(self):
        if QMessageBox.question(self, "Shutdown", "Really shut down?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            os.system("shutdown /s /t 5")

    def _show_info(self, t):
        if not self.wm.is_awake_status():
            self._add_chat("⚠️ I'm sleeping! Please say 'Wake Up' or type 'wake up' first.", "jarvis")
            self.voice.speak("Please wake me up first.")
            return
        
        now = datetime.datetime.now()
        if t == "time":
            msg = f"Time: {now.strftime('%I:%M:%S %p')}"
        elif t == "date":
            msg = f"Date: {now.strftime('%A, %B %d, %Y')}"
        elif t == "battery":
            try:
                bat = psutil.sensors_battery()
                msg = f"Battery: {bat.percent}%" if bat else "No battery"
            except:
                msg = "Battery info unavailable"
        elif t == "cpu":
            try:
                msg = f"CPU: {psutil.cpu_percent()}%"
            except:
                msg = "CPU info unavailable"
        else:
            return
        self._add_chat(msg, "jarvis")
        self.voice.speak(msg)

    def _chat_send(self):
        text = self.chat_input.text().strip()
        if not text:
            return
        self.chat_input.clear()
        self._add_chat(text, "user")
        
        if text.lower() == "wake up":
            self._manual_wake()
            return
        elif text.lower() in ["sleep", "go to sleep"]:
            self._manual_sleep()
            return
        
        if not self.wm.is_awake_status():
            self._add_chat("⚠️ I'm sleeping! Please type 'wake up' first to activate me.", "jarvis")
            return
        
        if not self._handle_text_command(text):
            self._target = "chat"
            self.ai.chat(text)

    def _handle_text_command(self, text):
        t = text.lower().strip()

        if t.startswith("play "):
            song = t.replace("play", "").strip()
            if song:
                self._play_quick(song)
                return True

        if t in ["chrome", "open chrome"]:
            self._syscmd("chrome")
            return True
        if t in ["youtube", "open youtube"]:
            self._syscmd("youtube")
            return True
        if t in ["spotify", "open spotify"]:
            self._syscmd("spotify")
            return True
        if t in ["calculator", "calc", "open calculator"]:
            self._syscmd("calc")
            return True
        if t in ["notepad", "open notepad"]:
            self._syscmd("notepad")
            return True
        if t in ["vscode", "vs code", "open vscode"]:
            self._syscmd("vscode")
            return True
        if t in ["explorer", "file explorer", "open explorer"]:
            self._syscmd("explorer")
            return True
        if t in ["stop music", "stop"]:
            self._syscmd("stop")
            return True
        if t in ["volume up", "vol up"]:
            self._syscmd("vol_up")
            return True
        if t in ["volume down", "vol down"]:
            self._syscmd("vol_down")
            return True
        if t in ["lock", "lock pc", "lock computer"]:
            self._syscmd("lock")
            return True
        if t in ["sleep pc", "sleep computer"]:
            self._syscmd("sleep")
            return True
        if t in ["restart", "reboot"]:
            self._syscmd("restart")
            return True
        if t in ["shutdown", "shut down"]:
            self._syscmd("shutdown")
            return True
        if t in ["time", "what time"]:
            self._show_info("time")
            return True
        if t in ["date", "what date"]:
            self._show_info("date")
            return True
        if t in ["battery", "battery status"]:
            self._show_info("battery")
            return True
        if t in ["cpu", "cpu usage"]:
            self._show_info("cpu")
            return True
        if t in ["help", "commands", "what can you do"]:
            self._add_chat(
                "🔴 IMPORTANT: You must say 'WAKE UP' or type 'wake up' FIRST!\n\n"
                "🎙️ VOICE COMMANDS (After saying 'Wake Up'):\n"
                "  • 'open chrome' - Opens Chrome\n"
                "  • 'open youtube' - Opens YouTube\n"
                "  • 'open spotify' - Opens Spotify\n"
                "  • 'open calculator' - Opens Calculator\n"
                "  • 'open notepad' - Opens Notepad\n"
                "  • 'open vs code' - Opens VS Code\n"
                "  • 'play shape of you' - Plays song on YouTube\n"
                "  • 'stop music' - Stops music\n"
                "  • 'volume up / volume down' - Adjust volume\n"
                "  • 'lock my pc' - Locks computer\n"
                "  • 'what time is it' - Tells time\n"
                "  • 'battery status' - Shows battery\n"
                "  • 'tell me a joke' - Tells a joke\n\n"
                "⌨️ CODING AI (40+ Languages):\n"
                "  • Generate code in any language\n"
                "  • Explain, Debug, Optimize code\n"
                "  • Convert between languages\n\n"
                "📝 TEXT COMMANDS (type in chat after 'wake up'):\n"
                "  • 'wake up' - Activate (required first!)\n"
                "  • 'sleep' - Deactivate\n"
                "  • 'help' - Shows this message", "jarvis"
            )
            return True

        return False

    def _add_chat(self, msg, who):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        colors = {"user": RED2, "jarvis": CYAN, "system": GREY}
        names = {"user": "YOU", "jarvis": "JARVISE", "system": "SYS"}
        c = colors.get(who, GREY)
        n = names.get(who, "?")
        self.chat_area.append(f'<span style="color:{c};font-weight:bold;">[{ts}] {n}:</span> {msg}')
        self.chat_area.append("─" * 50)
        self.chat_area.moveCursor(QTextCursor.End)

    def _clear_chat(self):
        self.chat_area.clear()
        self._add_chat("Chat cleared.", "system")

    def _ask_q(self):
        if not self.wm.is_awake_status():
            self.q_output.setPlainText("⚠️ I'm sleeping! Please say 'Wake Up' first.")
            return
            
        if not self.ai.is_available():
            self.q_output.setPlainText("❌ Ollama not connected.")
            return
        q = self.q_input.toPlainText().strip()
        if not q:
            return
        self._target = "question"
        self.ai.question(q)

    def _ai_response(self, resp):
        if self._target == "code":
            self.code_output.setPlainText(resp)
            self.code_status.setText("✅ Done.")
        elif self._target == "question":
            self.q_output.setPlainText(resp)
        else:
            self._add_chat(resp, "jarvis")
            self.voice.speak(resp[:300])
        self.footer_lbl.setText("✅ Response received")

    def _ai_thinking(self, thinking):
        self.footer_lbl.setText("🤔 Thinking..." if thinking else "Ready")

    def _ai_error(self, err):
        if self._target == "code":
            self.code_output.setPlainText(f"❌ Error: {err}")
            self.code_status.setText("❌ Error")
        elif self._target == "question":
            self.q_output.setPlainText(f"❌ Error: {err}")
        else:
            self._add_chat(f"Error: {err}", "system")

    def _voice_cmd(self, cmd):
        self._add_chat(f"🎤 {cmd}", "user")
        
        if not self.wm.is_awake_status():
            self._add_chat("⚠️ I'm not awake! Say 'Wake Up' first.", "jarvis")
            self.voice.speak("Please say Wake Up first.")
            return
        
        if cmd.lower().startswith("play "):
            song = cmd.lower().replace("play", "").strip()
            if song:
                self._play_quick(song)
        elif "open chrome" in cmd.lower() or cmd.lower() == "chrome":
            self._syscmd("chrome")
        elif "open youtube" in cmd.lower() or cmd.lower() == "youtube":
            self._syscmd("youtube")
        elif "open spotify" in cmd.lower() or cmd.lower() == "spotify":
            self._syscmd("spotify")
        elif "open calculator" in cmd.lower() or cmd.lower() == "calculator":
            self._syscmd("calc")
        elif "open notepad" in cmd.lower() or cmd.lower() == "notepad":
            self._syscmd("notepad")
        elif "open vs code" in cmd.lower() or "open code" in cmd.lower():
            self._syscmd("vscode")
        elif "open explorer" in cmd.lower():
            self._syscmd("explorer")
        elif "stop music" in cmd.lower():
            self._syscmd("stop")
        elif "volume up" in cmd.lower():
            self._syscmd("vol_up")
        elif "volume down" in cmd.lower():
            self._syscmd("vol_down")
        elif "lock" in cmd.lower():
            self._syscmd("lock")
        elif "sleep pc" in cmd.lower() or "sleep computer" in cmd.lower():
            self._syscmd("sleep")
        elif "restart" in cmd.lower():
            self._syscmd("restart")
        elif "shutdown" in cmd.lower():
            self._syscmd("shutdown")
        elif "what time" in cmd.lower() or "time" in cmd.lower():
            self._show_info("time")
        elif "what date" in cmd.lower() or "date" in cmd.lower():
            self._show_info("date")
        elif "battery" in cmd.lower():
            self._show_info("battery")
        elif "cpu" in cmd.lower():
            self._show_info("cpu")
        elif "joke" in cmd.lower() or "tell me a joke" in cmd.lower():
            jokes = ["Why don't programmers like nature? Too many bugs!", "What do you call a fake noodle? An impasta!"]
            joke = random.choice(jokes)
            self.voice.speak(joke)
            self._add_chat(joke, "jarvis")
        else:
            if any(k in cmd.lower() for k in ["code", "function", "write", "create", "program", "script"]):
                self.code_input.setPlainText(cmd)
                self.tabs.setCurrentIndex(4)
                self._code_action("generate")
            else:
                self.ai.chat(cmd)

    def _voice_status(self, s):
        self.voice_status.setText(s)

    def _on_wake_detected(self):
        self.wm.wake()
        self.awake_lbl.setText("🟢 AWAKE")
        self.awake_lbl.setStyleSheet(f"color:{CYAN}; font-size:{F_MED}px; font-weight:bold;")
        self.footer_lbl.setText("🟢 ACTIVATED - Ready for commands!")
        self._add_chat("🔊 Wake word detected! I'm now AWAKE. Say your command.", "jarvis")
        self.voice.speak("Yes sir, I'm awake.")

    def _manual_wake(self):
        self.wm.wake()
        self.awake_lbl.setText("🟢 AWAKE")
        self.awake_lbl.setStyleSheet(f"color:{CYAN}; font-size:{F_MED}px; font-weight:bold;")
        self.footer_lbl.setText("🟢 ACTIVATED - Ready for commands!")
        self._add_chat("🔊 I'm now AWAKE! You can say commands.", "jarvis")
        self.voice.speak("Yes sir, I'm awake and ready.")

    def _manual_sleep(self):
        self.wm.sleep()
        self.awake_lbl.setText("🔴 SLEEPING")
        self.awake_lbl.setStyleSheet(f"color:{RED2}; font-size:{F_MED}px; font-weight:bold;")
        self.footer_lbl.setText("🔴 SLEEPING - Say 'WAKE UP' to activate!")
        self._add_chat("😴 Going to sleep. Say 'Wake Up' to activate me.", "jarvis")
        self.voice.speak("Going to sleep sir.")

    def _update_sys(self):
        if self.ai.is_available():
            self.ai_status_lbl.setText(f"🤖 Ollama AI: ✅ Connected | Model: {self.ai.model}")
        else:
            self.ai_status_lbl.setText("🤖 Ollama AI: ❌ Not Connected — Run: ollama serve")

        if PSUTIL_AVAILABLE:
            try:
                cpu = psutil.cpu_percent()
                self.cpu_card.update(f"{cpu:.1f}%", cpu, "Good" if cpu < 60 else "High")
                ram = psutil.virtual_memory()
                self.ram_card.update(f"{ram.percent:.1f}%", ram.percent, "Normal" if ram.percent < 75 else "High")
                bat = psutil.sensors_battery()
                if bat:
                    self.bat_card.update(f"{int(bat.percent)}%", bat.percent, "Charging" if bat.power_plugged else "Battery")
            except:
                pass

    def _welcome(self):
        ok = self.ai.is_available()
        self._add_chat(
            f"⚡ JARVISE BLACK EDITION — CODING AI + SPOTIFY + WAKE COMMAND ⚡\n\n"
            f"   AI Status: {'✅ Connected' if ok else '❌ Not connected — run: ollama serve'}\n"
            f"   Coding AI: 40+ Programming Languages Supported!\n"
            f"   Spotify: Open Spotify desktop app or web player\n\n"
            f"🔴 IMPORTANT: You MUST say 'WAKE UP' or type 'wake up' FIRST!\n\n"
            f"🎤 After waking up, try:\n"
            f"   • 'open chrome' - Opens Chrome\n"
            f"   • 'open spotify' - Opens Spotify\n"
            f"   • 'play shape of you' - Plays music on YouTube\n"
            f"   • 'what time is it' - Tells time\n"
            f"   • 'write a Python function' - Generates code\n\n"
            f"⌨️ Coding AI Features:\n"
            f"   • Generate code in any language\n"
            f"   • Explain, Debug, Optimize code\n"
            f"   • Convert between languages\n\n"
            f"📝 Type 'help' for all commands\n"
            f"🔲 Press F11 for fullscreen", "jarvis"
        )
        if TTS_AVAILABLE:
            self.voice.speak("JARVISE Black Edition ready with Coding AI and Spotify. You must say Wake Up first before any command.")

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F11:
            self.showNormal() if self.isFullScreen() else self.showFullScreen()
        super().keyPressEvent(e)

    def closeEvent(self, e):
        if self.vw:
            self.vw.stop()
            self.vw.quit()
            self.vw.wait()
        e.accept()


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app.setStyle('Fusion')

    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(8, 8, 8))
    pal.setColor(QPalette.WindowText, QColor(255, 255, 255))
    pal.setColor(QPalette.Base, QColor(18, 18, 18))
    pal.setColor(QPalette.AlternateBase, QColor(26, 26, 26))
    pal.setColor(QPalette.Text, QColor(0, 255, 204))
    pal.setColor(QPalette.Button, QColor(20, 20, 20))
    pal.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    pal.setColor(QPalette.Highlight, QColor(200, 0, 0))
    pal.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(pal)

    w = Jarvise()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()