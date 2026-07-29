import sys
from PySide6.QtWidgets import (
    QApplication, 
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

def run():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("SmartFolder AI")
    window.resize(600, 400)

    layout = QVBoxLayout()

    title = QLabel("SmartFolder AI")
    status = QLabel("Watching...")

    start_button = QPushButton("Start")
    stop_button = QPushButton("Stop")
    settings_button = QPushButton("Settings")

    layout.addWidget(title)
    layout.addWidget(status)
    layout.addWidget(start_button)
    layout.addWidget(stop_button)
    layout.addWidget(settings_button)

    window.setLayout(layout)

    window.show()
    app.exec()