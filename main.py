# main.py

import sys
import os
import subprocess
import psutil
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QIcon, QPainter, QColor, QBrush, QPen, QAction

class MSIFanControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MSI Fan")
        self.setFixedSize(300, 200)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        icon_path = "media/fan_icon.png"
        self.setWindowIcon(QIcon(icon_path))

        # System tray configuration
        self.setup_system_tray(icon_path)

        # Timer confs for temp label
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temp)
        self.timer.start(2000) # 2 secs update

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(10)
        
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(0)
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(24, 24)
        self.btn_close.setObjectName("btn_close")
        self.btn_close.clicked.connect(self.close)
        
        self.btn_minimize = QPushButton('-')
        self.btn_minimize.setFixedSize(24, 24)
        self.btn_minimize.setObjectName("btn_minimize")
        self.btn_minimize.clicked.connect(self.minimize_to_tray)
        
        top_bar.addStretch() 
        top_bar.addWidget(self.btn_minimize)
        top_bar.addWidget(self.btn_close)
        
        container_top = QWidget()
        container_top.setLayout(top_bar)
        container_top.setFixedHeight(24)
        
        layout.addWidget(container_top)
        layout.addSpacing(5)
        
        self.label = QLabel("Status: Waiting for command...")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Temperature label
        self.temp_label = QLabel("")
        try:
            temps = psutil.sensors_temperatures()
            cpu_temps = temps.get('coretemp') or temps.get('acpi_thermal')
            
            if (cpu_temps):
                current_temp = cpu_temps[0].current
                self.temp_label.setText(f"Actual Temperature: {current_temp}°C")
            else:
                self.temp_label.setText("Sensors not found")
        except AttributeError:
            print("Your platform does not support sensor temperature readings.")
        
        self.temp_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.temp_label)

        self.btn_turbo = QPushButton("Activate Turbo Mode")
        self.btn_turbo.setObjectName("btn_turbo")
        self.btn_turbo.clicked.connect(lambda: self.run_isw("-b", "on", "Turbo Mode: ACTIVATED"))
        layout.addWidget(self.btn_turbo)

        self.btn_normal = QPushButton("Normal / Auto Mode")
        self.btn_normal.setObjectName("btn_normal")
        self.btn_normal.clicked.connect(lambda: self.run_isw("-b", "off", "Normal Mode: ACTIVATED"))
        layout.addWidget(self.btn_normal)

        self.setLayout(layout)

    def setup_system_tray(self, icon_path):
        """Init icon tray and menu context"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("MSI Fan Control")
        
        # Create the menu that appears when right-clicking the icon
        tray_menu = QMenu()
        
        action_show = QAction("Show Interface", self)
        action_show.triggered.connect(self.show_window)
        
        action_turbo = QAction("Turbo", self)
        action_turbo.triggered.connect(lambda: self.run_isw("-b", "on", "Turbo Mode: ACTIVATED"))
 
        action_normal = QAction("Normal", self)
        action_normal.triggered.connect(lambda: self.run_isw("-b", "off", "Normal Mode: ACTIVATED"))

 
        action_exit = QAction("Salir", self)
        action_exit.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(action_show)
        tray_menu.addSeparator()
        tray_menu.addAction(action_turbo)
        tray_menu.addSeparator()
        tray_menu.addAction(action_normal)
        tray_menu.addSeparator()
        tray_menu.addAction(action_exit)
        
        self.tray_icon.setContextMenu(tray_menu)

        # Intercept left-click/double-click on the tray icon
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        # Make the icon visible on the taskbar
        self.tray_icon.show()

    def minimize_to_tray(self):
        """Hide the main window"""
        self.hide()
        
    def show_window(self):
        """Restore the window and get front"""
        self.showNormal()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        """Handles the interaction with the icon"""
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def update_temp(self):
        temps = psutil.sensors_temperatures()
        cpu_temps = temps.get('coretemp') or temps.get('acpi_thermal')
        if cpu_temps:
            temp_list = [sensor.current for sensor in cpu_temps if sensor.current is not None]
            avg_temp = sum(temp_list) / len(temp_list)
            self.temp_label.setText(f"Actual Temperature: {avg_temp:.1f}°C")
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            window = self.windowHandle()
            if window:
                window.startSystemMove()
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        brush = QBrush(QColor("#1e1e1e"))
        painter.setBrush(brush)
        
        pen = QPen(QColor("#ffffff"))
        pen.setWidth(1)
        painter.setPen(pen)
        
        rect = self.rect().adjusted(0, 0, -1, -1)
        
        painter.drawRoundedRect(rect, 10, 10)

    def run_isw(self, flag, value, message):
        try:
            subprocess.run(["isw", flag, value], check=True)
            self.label.setText(message)
        except subprocess.CalledProcessError:
            self.label.setText("Error: Did you run with sudo/kdesu?")

def load_stylesheet(app):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(base_dir, "styles", "style.qss")
        
    try:
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print(f"Warning: style.qss not found at {qss_path}, using default style.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    
    load_stylesheet(app)
    
    window = MSIFanControl()
    window.show()
    sys.exit(app.exec())