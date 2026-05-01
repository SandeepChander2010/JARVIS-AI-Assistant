## **Bold Heading**JARVISE BLACK EDITION - AI CODING ASSISTANT


Advanced AI Voice Assistant with 40+ Programming Languages Support
Requires: Python 3.8+, Ollama, Microphone (for voice commands)

Section 2: FEATURES

🎤 VOICE CONTROL:
   - Wake word required: Say "WAKE UP" before any command
   - 40+ voice commands for system control
   - Text-to-speech responses
   - 2-minute auto sleep timeout

⌨️ CODING AI (40+ LANGUAGES):
   - Generate Code from natural language description
   - Explain Code step by step
   - Debug Code - find and fix errors
   - Optimize Code for performance
   - Convert Code between programming languages
   - Review Code professionally
   - Generate Unit Tests automatically
   - Add Documentation and docstrings

❓ QUESTION AI:
   - Ask any general knowledge questions
   - Get intelligent answers from AI
   - Topics include: Science, Technology, History, Math, How-To
   - Real-world examples and explanations
   - Natural conversation flow
   - Follow-up questions supported

🎵 YOUTUBE MUSIC:
   - Play any song by name
   - Quick play buttons for popular songs
   - Stop music playback
   - Volume control

🖥️ SYSTEM CONTROL:
   - Open Chrome, YouTube, Spotify, Calculator, Notepad, VS Code, File Explorer
   - Lock PC, Sleep PC, Restart, Shutdown
   - Volume Up/Down
   - Time and Date display

📊 SYSTEM MONITORING:
   - Real-time CPU usage
   - RAM usage monitoring
   - Battery status
   - Network connectivity

================================================================================
                            SYSTEM REQUIREMENTS
================================================================================

Minimum Requirements:
   - OS: Windows 10/11, Linux, or macOS
   - Python: 3.8 or higher
   - RAM: 8GB (16GB recommended for AI models)
   - Storage: 10GB free space
   - Internet: Required for YouTube & voice recognition

Optional but Recommended:
   - GPU for faster AI processing (NVIDIA with CUDA)
   - Microphone for voice commands
   - Speakers for voice responses

================================================================================
                          INSTALLATION GUIDE
================================================================================

STEP 1: Install Python
   - Download Python 3.8+ from: https://python.org
   - CHECK "Add Python to PATH" during installation

STEP 2: Install Required Python Packages

   Method A - One-Line Installation (Recommended):
   -------------------------------------------------
   pip install PyQt5 PyQtWebEngine pyttsx3 psutil pyautogui pywhatkit speechrecognition ollama

   Method B - Using pipwin for Audio Driver (Windows only):
   ---------------------------------------------------------
   pip install pipwin
   pipwin install pyaudio

   Method C - Verify Installation:
   -------------------------------
   python -c "import PyQt5, pyttsx3, psutil, pyautogui, pywhatkit, speech_recognition, ollama; print('OK')"

================================================================================
                            OLLAMA SETUP (REQUIRED)
================================================================================

Ollama is a free, local AI that runs on your computer. No internet required.

STEP 1: Download Ollama
   - Go to: https://ollama.ai/download
   - Download for your OS (Windows/Linux/macOS)
   - Install with default settings

STEP 2: Start Ollama Service
   Open a terminal and run:
   -------------------------------------------------
   ollama serve
   -------------------------------------------------
   Keep this terminal open!

STEP 3: Download AI Model (in another terminal)

   For Coding & Question AI (Recommended - 7B model):
   -------------------------------------------------
   ollama pull llama3.2:7b
   -------------------------------------------------

   For Best Coding (6.7B model - DeepSeek):
   -------------------------------------------------
   ollama pull deepseek-coder:6.7b
   -------------------------------------------------

   For Fast/Lightweight (1.3B model):
   -------------------------------------------------
   ollama pull deepseek-coder:1.3b
   -------------------------------------------------

STEP 4: Verify Ollama is Working
   -------------------------------------------------
   ollama list
   -------------------------------------------------
   Should show installed models

================================================================================
                          HOW TO USE JARVISE
================================================================================

STEP 1: Start Ollama (in first terminal)
   -------------------------------------------------
   ollama serve
   -------------------------------------------------

STEP 2: Run JARVISE (in second terminal)
   -------------------------------------------------
   python JARVIS.py
   -------------------------------------------------

STEP 3: Wake Up Jarvis
   - VOICE: Say "Wake Up"
   - TEXT: Type "wake up" in Chat tab
   - BUTTON: Click "⚡ Wake Up" button

STEP 4: Give Commands

   Voice Commands (After saying "Wake Up"):
   ----------------------------------------
   "open chrome"           - Opens Chrome browser
   "play shape of you"     - Plays music on YouTube
   "what time is it"       - Tells current time
   "lock my pc"            - Locks your computer
   "write a Python function" - Generates code
   "what is artificial intelligence" - Asks Question AI

   Text Commands (Type in CHAT tab after "wake up"):
   -------------------------------------------------
   open chrome
   open youtube
   open spotify
   what time is it
   what is quantum computing
   explain black holes
   help
   
================================================================================
                          VOICE COMMANDS LIST
================================================================================

🌐 BROWSER & APPS COMMANDS:
   "open chrome" / "chrome"        - Opens Google Chrome
   "open youtube" / "youtube"      - Opens YouTube
   "open spotify" / "spotify"      - Opens Spotify
   "open calculator" / "calculator" - Opens Calculator
   "open notepad" / "notepad"       - Opens Notepad
   "open vs code" / "vscode"        - Opens VS Code
   "open explorer" / "explorer"     - Opens File Explorer

🎵 MUSIC COMMANDS:
   "play [song name]"               - Plays song on YouTube
   "stop music"                     - Stops playback

🔊 VOLUME COMMANDS:
   "volume up" / "vol up"           - Increases volume
   "volume down" / "vol down"       - Decreases volume

🖥️ SYSTEM COMMANDS:
   "lock my pc" / "lock"            - Locks computer
   "sleep pc" / "sleep"             - Puts computer to sleep
   "restart" / "restart pc"         - Restarts computer
   "shutdown" / "shut down"         - Shuts down computer

ℹ️ INFORMATION COMMANDS:
   "what time is it" / "time"       - Shows current time
   "what date is it" / "date"       - Shows current date
   "battery status" / "battery"     - Shows battery percentage
   "cpu usage" / "cpu"              - Shows CPU usage

❓ QUESTION AI COMMANDS:
   "what is [topic]"                - Asks about any topic
   "who is [person]"                - Asks about a person
   "explain [concept]"              - Explains a concept
   "how does [thing] work"          - Explains how something works
   "tell me about [subject]"        - Provides information
   "compare [A] and [B]"            - Compares two things

😄 FUN COMMANDS:
   "tell me a joke"                 - Tells a random joke
   "hello" / "hi"                   - Greets you
   "how are you"                    - Responds with status

================================================================================
                          QUESTION AI FEATURES
================================================================================

HOW TO USE QUESTION AI:

Method 1 - QUESTION AI Tab:
  1. Click "? QUESTION AI" tab
  2. Select topic category (Science, Math, Technology, History, How To, Compare, General)
  3. Type your question in the input box
  4. Click "🚀 Ask AI" button
  5. Get intelligent answer from AI

Method 2 - Voice Commands:
  After saying "Wake Up":
  -------------------------------------------------
  "what is artificial intelligence"
  "explain quantum computing"
  "tell me about the Roman Empire"
  -------------------------------------------------

Method 3 - Chat Commands:
  Type in CHAT tab after "wake up":
  -------------------------------------------------
  what is machine learning
  how does a computer work
  explain blockchain technology
  -------------------------------------------------

QUESTION AI Features:
   • Natural language understanding
   • Detailed explanations with examples
   • Follow-up questions supported
   • Context-aware responses
   • Clear, structured answers
   • Real-time AI processing via Ollama
   
================================================================================
                          CODING AI FEATURES
================================================================================

HOW TO USE CODING AI:

Method 1 - Coding AI Tab:
  1. Click "⌨ CODING AI" tab
  2. Select your Programming Language (40+ options)
  3. Choose AI Model (deepseek-coder recommended)
  4. Enter your request or paste code
  5. Click action button:
     - Generate: Create code from description
     - Explain: Understand existing code
     - Debug: Find and fix errors
     - Optimize: Improve performance
     - Convert: Translate between languages
     - Review: Get code review
     - Tests: Generate unit tests
     - Document: Add documentation

Method 2 - Voice Commands:
  After saying "Wake Up":
  -------------------------------------------------
  "write a Python function to calculate factorial"
  "explain this code"
  "debug my function"
  -------------------------------------------------

Method 3 - Chat Commands:
  Type in CHAT tab after "wake up":
  -------------------------------------------------
  write a REST API in Python using Flask
  create a binary search tree in JavaScript
  -------------------------------------------------

================================================================================
                    SUPPORTED PROGRAMMING LANGUAGES (40+)
================================================================================

WEB LANGUAGES:
   HTML, CSS, SCSS, JavaScript, TypeScript, React/JSX, Vue, Angular, Svelte

BACKEND LANGUAGES:
   Python, Java, C#, PHP, Ruby, Go, Rust, Swift, Kotlin

SYSTEM LANGUAGES:
   C, C++, Assembly, Zig, Nim, V, Odin

DATA SCIENCE:
   R, MATLAB, Julia, SQL, Scala

MOBILE:
   Swift, Kotlin, Dart, Flutter, React Native

FUNCTIONAL:
   Haskell, Erlang, Elixir, F#, Clojure, OCaml, Scheme

SCRIPTING:
   Bash/Shell, PowerShell, Lua, Perl, Groovy

LEGACY:
   COBOL, Fortran, Pascal, Delphi, Ada

HARDWARE:
   Verilog, VHDL, SystemVerilog

OTHER:
   Solidity, VBA, Objective-C, Crystal, Nim

================================================================================
                          TROUBLESHOOTING
================================================================================

ISSUE 1: "Ollama not connected"
   SOLUTION: Start Ollama service
   -------------------------------------------------
   ollama serve
   -------------------------------------------------

ISSUE 2: PyAudio installation fails (Windows)
   SOLUTION: Use pipwin
   -------------------------------------------------
   pip install pipwin
   pipwin install pyaudio
   -------------------------------------------------

ISSUE 3: "speech_recognition not found"
   SOLUTION: Install speech recognition
   -------------------------------------------------
   pip install speechrecognition
   -------------------------------------------------

ISSUE 4: Microphone not working
   SOLUTION: Check microphone permissions
   - Windows: Settings > Privacy > Microphone > Allow apps to access

ISSUE 5: AI model too slow
   SOLUTION: Use smaller model
   -------------------------------------------------
   ollama pull deepseek-coder:1.3b
   -------------------------------------------------

ISSUE 6: Question AI not responding
   SOLUTION: Make sure Ollama is running and model is downloaded
   -------------------------------------------------
   ollama serve
   ollama pull llama3.2:7b
   -------------------------------------------------

ISSUE 7: Out of memory error
   SOLUTION: 
   - Close other applications
   - Use smaller AI model
   - Increase virtual memory

ISSUE 8: "No module named PyQt5"
   SOLUTION:
   -------------------------------------------------
   pip install PyQt5 PyQtWebEngine
   -------------------------------------------------

ISSUE 9: Voice commands not working
   SOLUTION:
   - Ensure microphone is connected
   - Say "Wake Up" first
   - Check microphone levels in Sound Settings
   - Speak clearly at normal volume

================================================================================
                          QUICK ACTION BUTTONS
================================================================================

QUICK ACTIONS TAB INCLUDES:

APPLICATIONS (7 buttons):
   🌐 Google Chrome  - Opens Chrome browser
   ▶ YouTube         - Opens YouTube website
   🎵 Spotify        - Opens Spotify
   🧮 Calculator     - Opens Windows Calculator
   📝 Notepad        - Opens Notepad
   💻 VS Code        - Opens Visual Studio Code
   📁 File Explorer  - Opens File Explorer

SYSTEM (4 buttons):
   🔒 Lock PC        - Locks your computer
   💤 Sleep PC       - Puts computer to sleep
   🔄 Restart        - Restarts computer
   ⏻ Shutdown       - Shuts down computer

INFO (4 buttons):
   🕐 Time           - Shows current time
   📅 Date           - Shows current date
   🔋 Battery        - Shows battery percentage
   💻 CPU            - Shows CPU usage

================================================================================
                          KEYBOARD SHORTCUTS
================================================================================

   F11          - Toggle Fullscreen mode
   Esc          - Exit Fullscreen
   Enter        - Send message (in Chat tab)

================================================================================
                          QUICK START SUMMARY
================================================================================

1. INSTALL PYTHON PACKAGES:
   -------------------------------------------------
   pip install PyQt5 pyttsx3 psutil pyautogui pywhatkit speechrecognition ollama
   pip install pipwin && pipwin install pyaudio
   -------------------------------------------------

2. INSTALL OLLAMA:
   Download from: https://ollama.ai/download

3. START OLLAMA:
   -------------------------------------------------
   ollama serve
   -------------------------------------------------

4. PULL AI MODELS:
   -------------------------------------------------
   ollama pull llama3.2:7b        # For Question AI
   ollama pull deepseek-coder:6.7b # For Coding AI
   -------------------------------------------------

5. RUN JARVISE:
   -------------------------------------------------
   python JARVISE.py
   -------------------------------------------------

6. SAY "WAKE UP" THEN COMMAND:
   -------------------------------------------------
   "open chrome"
   "play shape of you"
   "what is artificial intelligence"
   "write a Python function to sort a list"
   -------------------------------------------------

================================================================================
                              TIPS FOR BEST EXPERIENCE
================================================================================

1. Always say "Wake Up" first before any voice command
2. Speak clearly and at normal volume
3. Use a good microphone for better voice recognition
4. Close unused applications to free RAM for AI
5. Use deepseek-coder model for best coding results
6. Use llama3.2 model for best Question AI results
7. Type "help" in chat to see all commands
8. Use Coding AI tab for complex programming tasks
9. Use Question AI tab for general knowledge questions
10. You can ask follow-up questions - AI remembers context!

================================================================================
                          AVAILABLE AI MODELS
================================================================================

Model Name              Size    RAM Required    Best For
---------------------------------------------------------
deepseek-coder:1.3b     1GB     4GB            Fast coding (lightweight)
deepseek-coder:6.7b     4GB     8GB            Best coding (recommended)
deepseek-coder:33b      19GB    32GB           Maximum quality (powerful)
codellama:7b            4GB     8GB            General coding
codellama:13b           7GB     16GB           Better reasoning
llama3.2:7b             4GB     8GB            Question AI & General chat (recommended)
llama3.2:70b            40GB    64GB           Most capable (slower)
mistral:7b              4GB     8GB            Fast all-rounder

================================================================================
                              LICENSE
================================================================================

MIT License - Free for personal and commercial use

================================================================================
                              CREDITS
================================================================================

- Built with PyQt5
- AI powered by Ollama (DeepSeek-Coder, CodeLlama, Llama)
- Voice recognition by Google Speech API
- YouTube integration via pywhatkit

================================================================================
                              VERSION INFO
================================================================================

Version: 1.0
Last Updated: 2/5/2026
Author: SandeepChander.R

================================================================================
                    END OF README - HAPPY CODING!
================================================================================
