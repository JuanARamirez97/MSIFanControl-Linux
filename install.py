import os
import getpass

base_path = os.getcwd()
username = getpass.getuser()
desktop_file_path = os.path.expanduser(f"~/.local/share/applications/msi-fan.desktop")

desktop_content = f"""[Desktop Entry]
Name=MSI Fan Control
Comment=Controlador manual de ventiladores MSI
Exec=kdesu {base_path}/.venv/bin/python {base_path}/main.py
Icon={base_path}/fan_icon.png
Terminal=false
Type=Application
Categories=System;Utility;
"""

def create_desktop_file():
    try:
        with open(desktop_file_path, "w") as f:
            f.write(desktop_content)
        
        os.chmod(desktop_file_path, 0o755)
        
        print(f"Success! .desktop file created at: {desktop_file_path}")
        print("You should now see 'MSI Fan Control' in your application menu.")
    except Exception as e:
        print(f"Error creating file: {e}")

if __name__ == "__main__":
    create_desktop_file()