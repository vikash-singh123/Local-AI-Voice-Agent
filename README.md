# 🎙️ Local Voice Agent (v1.0.0)

A 100% offline, privacy-first AI voice-to-text agent for Windows. Hold F8, speak, and watch it type perfectly formatted text into any app. No cloud APIs, no subscriptions, no data leaving your machine.

##  Features
- **100% Local & Private:** Uses local Whisper and Llama 3.2 models. Zero internet required after setup.
- **Multilingual:** Supports English and Hindi/Hinglish.
- **System-Wide:** Types directly into Notepad, Slack, Word, or any text field via clipboard injection.
- **Smart Formatting:** Automatically fixes grammar, punctuation, and translates spoken Hindi to professional English.

##  How to Install & Run
1. Download the `LocalVoiceAgent_v1.0.zip` from the [Releases Page](https://github.com/vikash-singh123/Local-AI-Voice-Agent/releases).
2. Extract the zip file to a folder on your Desktop.
3. **Right-click** `RUN_AS_ADMIN.bat` and select **Run as Administrator**.
4. Open any text app (like Notepad) and click inside it.
5. **Hold the `F8` key**, speak your sentence, and **release `F8`**.
6. Click back into your text app to see the typed text!

## ⚠️ Important Windows Warnings
- **Windows SmartScreen:** Because this is an independent project without a paid corporate code-signing certificate, Windows might show a blue "Windows protected your PC" screen. Click **More Info** -> **Run Anyway**.
- **Admin Rights:** The app requires Admin privileges *strictly* to listen for the global F8 hotkey. It does not log keystrokes.

## 🔒 Privacy & Security
- **No Telemetry:** This app does not send your voice, text, or any data to the cloud. 
- **Open Source:** If you do not trust the compiled `.exe`, you can run the Python source code directly. See `final_agent.py` in this repository.
- **VirusTotal Scan:** [View the clean VirusTotal scan for the .exe here](https://www.virustotal.com/gui/file/bd675e2dea6e208fe5914ea3432f96304cef0c3ceb1f6cf9f2498cd1ae095a57/detection)

## 🛠️ Tech Stack
- Python 3.12
- `faster-whisper` (Base model for multilingual transcription)
- `llama-cpp-python` (Llama 3.2 1B Instruct GGUF for local text cleanup)
- `pyperclip` & `sounddevice`

## 🐛 Known Issues & Feedback
- The 1B parameter model is very fast but occasionally adds conversational filler. 
- I am actively looking for feedback! Please open an Issue on this repo if you find bugs or have feature requests.

## 📝 License
MIT License - Feel free to use, modify, and distribute!
