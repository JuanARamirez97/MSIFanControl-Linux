import os
import subprocess

def update_project():
    print("--- Starting update process ---")
    
    subprocess.run(["git", "pull", "origin", "main"], check=True)

    print("--- Updating dependencies ---")
    venv_python = os.path.join(os.getcwd(), ".venv", "bin", "python3")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)

    desktop_file = os.path.expanduser("~/.local/share/applications/msi-fan.desktop")
    if os.path.exists(desktop_file):
        os.remove(desktop_file)
    
    subprocess.run(["python3", "install.py"], check=True)
    print("--- Update complete! ---")