# FormCheck 🏋️
**AI-powered bodyweight exercise form analyzer**

---

## What it does
- Opens your webcam and tracks your body in real time using Google MediaPipe
- Shows a **green banner** when your form is correct
- Shows **red/yellow feedback** telling you exactly which body part to adjust
- Supports: Squats, Push-Ups, Lunges, Planks

---

## Setup (do this once)

### Step 1 — Install Python
Download Python 3.10 or 3.11 from https://python.org/downloads
During install, check ✅ "Add Python to PATH"

### Step 2 — Open a terminal
- **Windows**: Search "Command Prompt" in Start
- **Mac**: Search "Terminal" in Spotlight

### Step 3 — Navigate to this folder
```
cd path/to/formcheck
```
(Tip: drag the folder into the terminal window to auto-fill the path)

### Step 4 — Install dependencies
```
pip install -r requirements.txt
```
This downloads MediaPipe, OpenCV, and NumPy. Takes 1–3 minutes.

### Step 5 — Run it!
```
python main.py
```

---

## Controls
| Key | Action |
|-----|--------|
| `1` | Squat |
| `2` | Push-Up |
| `3` | Lunge |
| `4` | Plank |
| `M` | Toggle exercise menu |
| `Q` | Quit |

---

## Tips for best results
- Stand **2–3 metres** from your camera so your full body is visible
- Make sure you have **good lighting** (face a window or lamp)
- Wear **fitted clothing** — baggy clothes confuse the pose detector
- For push-ups and planks, a **side-angle** camera view works better

---

## File structure
```
formcheck/
├── main.py              ← Run this file
├── requirements.txt     ← Dependencies
├── utils.py             ← Angle calculation helpers
├── exercises/
│   ├── squat.py         ← Squat form rules
│   ├── pushup.py        ← Push-up form rules
│   ├── lunge.py         ← Lunge form rules
│   └── plank.py         ← Plank form rules
└── ui/
    └── overlay.py       ← Green/red HUD display
```

---

## Troubleshooting
**"Camera not found"** → Make sure no other app is using your webcam  
**"ModuleNotFoundError"** → Re-run `pip install -r requirements.txt`  
**Laggy / slow** → Close other apps; reduce webcam resolution in main.py (change 1280/720 to 640/480)
