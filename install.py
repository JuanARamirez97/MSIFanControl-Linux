import os
import subprocess
import sys
import getpass

base_path = os.getcwd()
venv_path = os.path.join(base_path, ".venv")
pip_path = os.path.join(venv_path, "bin", "pip")
python_path = os.path.join(venv_path, "bin", "python")

def setup_all():
    print("--- Setting up environment ---")
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    
    print("--- Installing dependencies ---")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    
    desktop_file_path = os.path.expanduser("~/.local/share/applications/msi-fan.desktop")
    desktop_content = f"""[Desktop Entry]
Name=MSI Fan Control
Comment=Manual MSI fan controller
Exec=kdesu {python_path} {base_path}/main.py
Icon={base_path}/media/fan_icon.png
Terminal=false
Type=Application
Categories=System;Utility;
"""
    with open(desktop_file_path, "w") as f:
        f.write(desktop_content)
    os.chmod(desktop_file_path, 0o755)
    print(f"Success! Installed at {desktop_file_path}")

if __name__ == "__main__":
    setup_all()