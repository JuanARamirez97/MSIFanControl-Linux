import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class MSIFanControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MSI Fan")
        self.setFixedSize(350, 200)
        
        self.setWindowIcon(QIcon("media/fan_icon.png"))

        layout = QVBoxLayout()

        self.label = QLabel("Status: Waiting for command...")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.btn_turbo = QPushButton("Activate Turbo Mode")
        self.btn_turbo.clicked.connect(lambda: self.run_isw("-b", "on", "Turbo Mode: ACTIVATED"))
        layout.addWidget(self.btn_turbo)

        self.btn_normal = QPushButton("Normal / Auto Mode")
        self.btn_normal.clicked.connect(lambda: self.run_isw("-b", "off", "Normal Mode: ACTIVATED"))
        layout.addWidget(self.btn_normal)

        self.setLayout(layout)

        # --- Estilo ---
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #333333;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton#btn_turbo:hover {
                background-color: #d32f2f;
            }
            QLabel {
                font-weight: bold;
                margin: 10px;
                color: #00bcd4;
            }
        """)

    def run_isw(self, flag, value, message):
        try:
            subprocess.run(["isw", flag, value], check=True)
            self.label.setText(message)
        except subprocess.CalledProcessError:
            self.label.setText("Error: Did you run with sudo/kdesu?")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplicar una paleta oscura global
    app.setStyle("Fusion") 
    
    window = MSIFanControl()
    window.show()
    sys.exit(app.exec())