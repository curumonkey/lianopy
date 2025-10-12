import argparse
import os
import socket
import uvicorn
import qrcode


def get_local_ip():
    """Get the local IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def main():
    parser = argparse.ArgumentParser(description="boilerplate CLI")  # EDIT: project name
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="Directory to serve (default: current working directory)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port to run on")
    args = parser.parse_args()

    os.environ["LIANOPY_STORAGE"] = args.directory   # EDIT: env var prefix

    ip = get_local_ip()
    url = f"http://{ip}:{args.port}"
    print(f"📂 Sharing {args.directory}")
    print(f"🌐 Access it at: {url}")

    # Generate and display QR code in terminal
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)  # prints a scannable QR code in terminal

    # Run the FastAPI app
    uvicorn.run("lianopy.app:app", host="0.0.0.0", port=args.port, reload=False)  # EDIT: package path


if __name__ == "__main__":
    main()
