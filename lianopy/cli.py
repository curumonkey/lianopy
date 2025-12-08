import argparse
import os
import socket
import uvicorn
import qrcode
import psutil
import inquirer
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".lianopy_config.json"


def get_local_ip():
    """Get the local IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def save_default(path: str):
    CONFIG_FILE.write_text(json.dumps({"default_path": str(path)}))


def load_default() -> str | None:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text()).get("default_path")
        except Exception:
            return None
    return None


def list_drives_and_common():
    """Detect drives and common user folders."""
    drives = []
    for p in psutil.disk_partitions(all=False):
        drives.append(p.mountpoint)

    common = {
        "Documents": os.path.expanduser("~/Documents"),
        "Pictures": os.path.expanduser("~/Pictures"),
        "Videos": os.path.expanduser("~/Videos"),
        "Desktop": os.path.expanduser("~/Desktop"),
        "Downloads": os.path.expanduser("~/Downloads"),
    }
    return drives, common


def choose_directory():
    """Interactive menu for choosing directory."""
    choices = ["Share this path", "Other Paths", "Default Path"]
    answer = inquirer.list_input("Choose an option:", choices=choices)

    if answer == "Share this path":
        return os.getcwd()

    elif answer == "Other Paths":
        drives, common = list_drives_and_common()
        subchoices = []
        subchoices.extend(drives)
        subchoices.extend([f"{k}: {v}" for k, v in common.items()])
        subchoices.append("Set Default Path")

        chosen = inquirer.list_input("Select a drive or folder:", choices=subchoices)

        if chosen == "Set Default Path":
            path = inquirer.text("Enter path to set as default:")
            save_default(path)
            print(f"✅ Default path set to {path}")
            return path

        if ": " in chosen:
            # common folder
            return chosen.split(": ", 1)[1]
        return chosen

    elif answer == "Default Path":
        default = load_default()
        if default:
            print(f"📌 Using default path: {default}")
            return default
        else:
            print("⚠️ No default path set. Falling back to current directory.")
            return os.getcwd()


def main():
    parser = argparse.ArgumentParser(description="Lianopy CLI")
    parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    args = parser.parse_args()

    directory = choose_directory()
    os.environ["LIANOPY_STORAGE"] = directory

    ip = get_local_ip()
    url = f"http://{ip}:{args.port}"
    print(f"📂 Sharing {directory}")
    print(f"🌐 Access it at: {url}")

    # Generate and display QR code in terminal
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    # Run the FastAPI app
    uvicorn.run("lianopy.app:app", host="0.0.0.0", port=args.port, reload=False)


if __name__ == "__main__":
    main()
