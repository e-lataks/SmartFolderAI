import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QCheckBox,
    QLineEdit,
    QFileDialog
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

    back_button = QPushButton("Back")


    history_title = QLabel("History")
    history_list = QLabel()

    history_layout.addWidget(back_button)
    history_layout.addWidget(history_title)
    history_layout.addWidget(history_list)


    settings_page = QWidget()
    settings_layout = QVBoxLayout(settings_page)

    settings_back_button = QPushButton("Back")
    settings_title = QLabel("Settings")

    folder_label = QLabel("Watched folder:")

    folder_input = QLineEdit()
    folder_input.setText("watched")

    choose_folder_button = QPushButton("Choose folder")

    sort_checkbox = QCheckBox("Sort files into AI folders")
    sort_checkbox.setChecked(False)

    save_setting_button = QPushButton("Save")

    settings_layout.addWidget(settings_back_button)
    settings_layout.addWidget(settings_title)
    settings_layout.addWidget(folder_label)
    settings_layout.addWidget(folder_input)
    settings_layout.addWidget(choose_folder_button)
    settings_layout.addWidget(sort_checkbox)
    settings_layout.addWidget(save_setting_button)

    settings_button.clicked.connect(
        lambda: stack.setCurrentWidget(settings_page)
    )

    settings_back_button.clicked.connect(
        lambda: stack.setCurrentWidget(main_page)
    )

    def choose_folder():
        folder = QFileDialog.getExistingDirectory(
            window,
            "Choose folder"
        )
        if folder:
            folder_input.setText(folder)

    def save_settings():
        settings = {
            "watch_folder": folder_input.text(),
            "sort_into_folders": sort_checkbox.isChecked()
        }

        with open("data/config.json", "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)

        print("Settings saved:", settings)

    choose_folder_button.clicked.connect(choose_folder)
    save_setting_button.clicked.connect(save_settings)


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
                    f"Location: {item.get('watch_folder', 'Unknwon')}\n"
                    f"AI Category: {item['folder']}\n"
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
    stack.addWidget(settings_page)

 
    window_layout = QVBoxLayout()
    window_layout.addWidget(stack)

    window.setLayout(window_layout)

    window.show()
    app.exec()