# main.py

import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class MSIFanControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MSI Fan")
        self.setFixedSize(300, 200)
        self.setWindowIcon(QIcon("media/fan_icon.png"))

        layout = QVBoxLayout()

        self.label = QLabel("Status: Waiting for command...")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Asignamos nombres de objeto (ID) para el estilo específico
        self.btn_turbo = QPushButton("Activate Turbo Mode")
        self.btn_turbo.setObjectName("btn_turbo")
        self.btn_turbo.clicked.connect(lambda: self.run_isw("-b", "on", "Turbo Mode: ACTIVATED"))
        layout.addWidget(self.btn_turbo)

        self.btn_normal = QPushButton("Normal / Auto Mode")
        self.btn_normal.setObjectName("btn_normal")
        self.btn_normal.clicked.connect(lambda: self.run_isw("-b", "off", "Normal Mode: ACTIVATED"))
        layout.addWidget(self.btn_normal)

        self.setLayout(layout)

    def run_isw(self, flag, value, message):
        try:
            subprocess.run(["isw", flag, value], check=True)
            self.label.setText(message)
        except subprocess.CalledProcessError:
            self.label.setText("Error: Did you run with sudo/kdesu?")

def load_stylesheet(app):
    try:
        with open("styles/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: style.qss not found, using default style.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    # Cargar estilo externo
    load_stylesheet(app)
    
    window = MSIFanControl()
    window.show()
    sys.exit(app.exec())