import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget
)
from watcher import start_watching, stop_watching

def run():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("SmartFolder AI")
    window.resize(600, 400)

    stack = QStackedWidget()

    main_page = QWidget()
    layout = QVBoxLayout(main_page)

    title = QLabel("SmartFolder AI")
    status = QLabel("Stopped")

    start_button = QPushButton("Start")
    stop_button = QPushButton("Stop")
    history_button = QPushButton("History")
    settings_button = QPushButton("Settings")

    stop_button.setEnabled(False)

    layout.addWidget(title)
    layout.addWidget(status)
    layout.addWidget(start_button)
    layout.addWidget(stop_button)
    layout.addWidget(history_button)
    layout.addWidget(settings_button)


    history_page = QWidget()
    history_layout = QVBoxLayout(history_page)

    back_button = QPushButton("← Back")


    history_title = QLabel("History")
    history_list = QLabel()

    history_layout.addWidget(back_button)
    history_layout.addWidget(history_title)
    history_layout.addWidget(history_list)


    def start():
        start_watching()
        status.setText("Watching...")
        start_button.setEnabled(False)
        stop_button.setEnabled(True)

    def stop():
        stop_watching()
        status.setText("Stopped")
        start_button.setEnabled(True)
        stop_button.setEnabled(False)

    def load_history():
        try:
            with open("data/history.json", "r", encoding="utf-8") as file:
                history = json.load(file)

            if not history:
                history_list.setText("History is empty")
                return

            text = ""

            for item in reversed(history):
                text += (
                    f"Time: {item['time']}\n"
                    f"Old name: {item['old_name']}\n"
                    f"New name: {item['new_name']}\n"
                    f"Folder: {item['folder']}\n"
                    f"{'-' * 35}\n"
    )
            history_list.setText(text)
        except FileNotFoundError:
            history_list.setText("history.json not found.")

        except Exception as e:
            history_list.setText(str(e))


    start_button.clicked.connect(start)
    stop_button.clicked.connect(stop)

    def open_history():
        load_history()
        stack.setCurrentWidget(history_page)
    history_button.clicked.connect(open_history)


    back_button.clicked.connect(
        lambda: stack.setCurrentWidget(main_page)
    )


    stack.addWidget(main_page)
    stack.addWidget(history_page)

 
    window_layout = QVBoxLayout()
    window_layout.addWidget(stack)

    window.setLayout(window_layout)

    window.show()
    app.exec()