Once cloned

rename the "boilerplate" folder and "boilerplate" in pyproject.toml to your preferred project name.

cd to your project

then run this

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

navigate the folder or drive path you want to share in your local network
and type 
boilerplate
    
scan the qrcode or proceed to the url project

# 📦 Liana

**Liana** is a lightweight, **FastAPI‑powered** local file sharing server with a simple **CLI**.  
It lets you share any folder on your machine over your local network with a clean **web UI** and bundled **static assets**.

---

## 🚀 Features

- **Share any folder** on your LAN with one command  
- **FastAPI + Uvicorn** backend  
- **Static frontend assets** bundled inside the package  
- **CLI entry point** (`liana`) for convenience  
- **Cross‑platform** (Linux, macOS, Windows, iOS shells like iSH/Termux)  
- **Deployment‑ready** with `pyproject.toml` packaging  

---

## 📂 Project Structure

**liana-project/ ← project root**

**├── pyproject.toml ← packaging & metadata**

**├── requirements.txt ← dependencies**

**├── README.md ← this file**

**├── liana/ ← Python package**

**│ ├── init.py**

**│ ├── app.py ← FastAPI app** 

**│ ├── cli.py ← CLI entry point** 

**│ ├── config.py ← optional settings** 

**│ └── static/ ← bundled frontend assets** 

**└── .venv/ ← virtual environment (for dev)**


---

## ⚙️ Installation

**1. Clone and enter project**
git clone https://github.com/yourname/liana-project.git
cd liana-project

**2. Create and activate virtual environment**
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

**3. Install dependencies**
pip install -r requirements.txt

**4. (Optional) Install in editable mode**
pip install -e .

## 🖥️ Usage

**From any folder you want to share:**
cd ~/Pictures
liana

Output:
📂 Sharing /home/solo/Pictures
🌐 Access it at: http://192.168.1.42:8000
Open the printed URL in your browser to access the shared files.

## 🔧 CLI Options

liana [directory] [--port PORT]
directory → folder to share (default: current working directory)

--port → port to run on (default: 8000)

Example:

liana ~/Documents --port 9000
🧭 Customization Checklist (for future projects)
When reusing this boilerplate:

Rename project

Outer folder: newproject/

Inner package: newproject/

Update metadata

[project].name, description, authors, version in pyproject.toml

README.md title and description

Adjust CLI (cli.py)

Parser description

Env var prefix (NEWPROJECT_STORAGE)

Uvicorn import path (newproject.app:app)

Adjust FastAPI app (app.py)

FastAPI(title="...")

Default routes

Static mounts

Dependencies

Add/remove packages in pyproject.toml → [project].dependencies

Static assets

Place frontend files in static/

Add to [tool.setuptools.package-data] if you add templates or other assets

Runtime data

Keep runtime‑only folders (like storage_root/) outside the package so they aren’t bundled

📦 Deployment Options
venv → best for development

pipx → best for global CLI convenience (pipx install .)

Global pip → possible but less safe (pip install . with --break-system-packages on Debian/Ubuntu)

📜 License
MIT (or your choice)

Code

---

✨ This version is **GitHub‑ready**: bold highlights for readability, consistent code blocks, and clear sectioning.  

Would you like me to also add a **badges section** (e.g., Python version, FastAPI, license) at the top so it looks even more professional when people land on your repo?