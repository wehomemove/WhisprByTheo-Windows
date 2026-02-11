# WhisprByTheo for Windows 🎙️

**Push-to-talk voice transcription for Windows.** Hold a key to record, release to transcribe and paste. Works everywhere - Slack, email, documents, anywhere you can type.

<p align="center">
  <img src="https://img.shields.io/badge/Windows-10%2F11-blue?style=for-the-badge&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/OpenAI-Whisper_API-412991?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/100%25_Free-Open_Source-orange?style=for-the-badge" alt="Free">
</p>

---

## ✨ Features

| | |
|---|---|
| 🎙️ **Push-to-talk** | Hold F8 (or any key), speak, release - text appears |
| ⚡ **Fast** | ~1-2 seconds via OpenAI's Whisper API |
| 🎨 **Beautiful** | Sleek animated overlay with visual feedback |
| 🌍 **Any language** | Whisper supports 90+ languages |
| 💰 **Cheap** | ~$0.006/minute - basically free |

---

## 🖥️ Demo

<p align="center">
  <img src="https://raw.githubusercontent.com/wehomemove/WhisprByTheo.spoon/main/demo.gif" alt="WhisprByTheo Demo" width="150">
</p>

- 🔴 **Listening** - Red pulsing bars while recording
- 🔵 **Transcribing** - Blue flowing wave while processing
- ✅ **Done** - Green checkmark, text pasted

---

## 📋 Requirements

- **Windows 10 or 11**
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **OpenAI API key** ([Get one free](https://platform.openai.com/api-keys))
- **Microphone**

---

## 🚀 Installation

### Step 1: Install Python

If you don't have Python:
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11 or later
3. **Important:** Check ✅ "Add Python to PATH" during installation

### Step 2: Download WhisprByTheo

**Option A - Git:**
```cmd
git clone https://github.com/wehomemove/WhisprByTheo-Windows.git
cd WhisprByTheo-Windows
```

**Option B - Manual:**
1. [Download ZIP](https://github.com/wehomemove/WhisprByTheo-Windows/archive/refs/heads/main.zip)
2. Extract to a folder

### Step 3: Install Dependencies

Double-click `install.bat` or run:
```cmd
pip install -r requirements.txt
```

### Step 4: Get OpenAI API Key

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create an account (free)
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### Step 5: Run

Double-click `run.bat` or:
```cmd
python whispr.py
```

On first run, paste your OpenAI API key when prompted.

---

## 🎤 How to Use

1. **Hold F8** (or your configured key)
2. **Speak** - you'll see the red "Listening" animation
3. **Release F8**
4. Wait ~1-2 seconds
5. ✨ Text appears at your cursor

Works in any app!

---

## ⚙️ Configuration

Config is saved at `%USERPROFILE%\.config\whispr\config.json`

### Change Hotkey

Edit the config file:
```json
{
  "api_key": "sk-...",
  "hotkey": "f9"
}
```

Common hotkey options: `f1`-`f12`, `ctrl+shift+space`, `pause`, etc.

### Reset API Key

Delete the config file and restart:
```cmd
del %USERPROFILE%\.config\whispr\config.json
python whispr.py
```

---

## ❓ Troubleshooting

<details>
<summary><b>"pip is not recognized"</b></summary>

Python wasn't added to PATH. Reinstall Python and check "Add Python to PATH".
</details>

<details>
<summary><b>PyAudio install fails</b></summary>

Try:
```cmd
pip install pipwin
pipwin install pyaudio
```
</details>

<details>
<summary><b>No audio recorded</b></summary>

1. Check your microphone is set as default in Windows Settings → Sound → Input
2. Make sure no other app is using the microphone exclusively
</details>

<details>
<summary><b>API error</b></summary>

- Check your API key is correct
- Make sure you have credits in your OpenAI account
- Check your internet connection
</details>

---

## 💰 Cost

OpenAI Whisper API costs **$0.006 per minute** of audio.

| Usage | Cost |
|-------|------|
| 10 mins/day | ~$1.80/month |
| 30 mins/day | ~$5.40/month |
| 1 hour/day | ~$10.80/month |

Basically free for normal use.

---

## 🔒 Privacy

- Audio is sent to OpenAI for transcription
- OpenAI does not use API data to train models ([policy](https://openai.com/policies/api-data-usage-policies))
- Audio is not stored after transcription
- Your API key is stored locally only

For 100% local/private transcription, see the [Mac version](https://github.com/wehomemove/WhisprByTheo.spoon) (Apple Silicon only).

---

## 🙏 Credits

- [OpenAI Whisper](https://openai.com/research/whisper) - Speech recognition
- Built by Theo @ [Homemove](https://homemove.com)

---

## 📄 License

MIT - Use it however you want, free forever.
