# 🌿 Lianopy

A jungle‑themed, stateless, cross‑platform Python file‑sharing server.  
This project provides a **CLI + web interface** for sharing files across your local network with QR code onboarding, responsive UI, and secure storage handling.

---

## 📦 Features
- 🌐 Share any folder or drive path over your LAN  
- 📱 Scan a QR code for instant mobile access  
- ⚡ FastAPI backend with Uvicorn server  
- 🖥️ CLI for quick setup and control
- 🪶 Lightweight, cross‑platform, and easy to extend  

---

## 🚀 Getting Started

Clone our Lianopy repository

```bash
git clone https://github.com/<your-username>/lianopy.git <project name>
```

go to your project

```bash
cd <project name>
```

then run this

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Navigate to the folder you want to share Use the cd (change directory) command to move into the directory you’d like to make available on your local network. 

For example, on Windows:
```bash
# Example: share your "Downloads" folder
cd ~/Downloads
```

On Linux/macOS, you might use:
```bash
cd /home/yourname/Downloads
```


scan the qrcode or proceed to the url project
