# 🌿 Lianopy

### 🙈🍌 “Ooo‑oooh, welcome to my jungle! 

I’m just a curious monkey with a camera in hand. I love snapping photos of everything I see — but when it’s time to share them, the trouble begins:

- Everyone wants their own copy of the pictures.

- Online storage is too expensive for my big, juicy files.

- I don’t want to keep making new Gmail accounts just to pass things around. Are you guilty?

- And honestly… isn’t it amazing to share without being chained to the internet all the time?

That’s why I went swinging through the vines and found this clever thing called Lianopy. You know how we monkeys leap from liana to liana high up in the canopy? Well, that’s the idea here!

Instead of bananas, we’re sharing files — swinging them safely from one canopy to another through digital vines.

---

+ 🐒 Stateless & cross‑platform → works anywhere, no heavy baggage.

+ 🌐 CLI + Web interface → easy to start from the ground or the treetops.

+ 📱 QR code onboarding → just point, scan, and swing right in.

+ 🌴 Local network file sharing → pass files from canopy to canopy without needing the cloud. 

+ ⚡ Responsive UI & secure storage → smooth like a monkey’s swing, safe like a sturdy branch.

So when you run Lianopy, you’re not just starting a server — you’re opening a jungle bridge, letting others climb across and grab what they need. From canopy to canopy, vine to vine, the jungle stays connected.” 🌴

---

## 🚀 Getting Started

### for non-termux

Clone our Lianopy repository

```bash
git clone https://github.com/curumonkey/lianopy.git <project name>
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

Navigate to the folder you want to share.
Use the cd (change directory) command to move into the directory you’d like to make available on your local network. 

For example, on Windows:
```bash
# Example: share your "Downloads" folder
cd ~/Downloads
```

On Linux/macOS, you might use:
```bash
cd /home/yourname/Downloads
```

<<<<<<< HEAD
Scan the qrcode or proceed to the url project
=======

scan the qrcode or proceed to the url project


### for Termux

In you Termux

install proot-distro
```bash
pkg install proot-distro
```

install ubuntu
```bash
proot-distro install ubuntu
```

enable Termux Storage Access
```bash
termux-setup-storage
```

login to Ubuntu with a bind mount
```bash
proot-distro login ubuntu --bind /sdcard:/mnt/sdcard
```

install git inside ubuntu
```bash
apt install git
```


>>>>>>> 0e82ee1 (for termux)
