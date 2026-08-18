import sys
import tempfile
import json
import os

from PySide6.QtCore import Qt, QLockFile
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QStackedWidget,
    QCheckBox,
    QLineEdit,
    QFileDialog,
    QListWidget,
    QHBoxLayout,
    QSystemTrayIcon,
    QMenu
)
from watcher import start_watching, stop_watching
from PySide6.QtGui import QIcon, QAction


def resource_path(path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, path)


def run():
    app = QApplication(sys.argv)

    lock_path = os.path.join(
        tempfile.gettempdir(),
        "SmartFolderAI.lock"
    )

    lock = QLockFile(lock_path)

    if not lock.tryLock(100):
        app.quit()
        return

    app.setQuitOnLastWindowClosed(False)

    with open(
        resource_path("style.qss"),
        "r",
        encoding="utf-8"
    ) as file:
        app.setStyleSheet(file.read())

    window = QWidget()
    window.setWindowTitle("SmartFolder AI")
    window.resize(600, 400)
    window.setWindowIcon(
        QIcon(resource_path("assets/icon.ico"))
    )

    stack = QStackedWidget()

    tray = QSystemTrayIcon(
        QIcon(resource_path("assets/icon.ico")),
        window
    )

    tray_menu = QMenu()

    open_action = QAction("Open")
    start_action = QAction("Start")
    stop_action = QAction("Stop")
    quit_action = QAction("Quit")

    tray_menu.addAction(open_action)
    tray_menu.addSeparator()
    tray_menu.addAction(start_action)
    tray_menu.addAction(stop_action)
    tray_menu.addSeparator()
    tray_menu.addAction(quit_action)

    tray.setContextMenu(tray_menu)
    tray.show()

    main_page = QWidget()
    layout = QVBoxLayout(main_page)

    layout.setContentsMargins(50, 40, 50, 40)
    layout.setSpacing(12)

    title = QLabel("SmartFolder AI")
    status = QLabel("Stopped")

    title.setObjectName("title")
    status.setObjectName("status")

    start_button = QPushButton("Start")
    start_button.setObjectName("startButton")

    stop_button = QPushButton("Stop")
    history_button = QPushButton("History")
    settings_button = QPushButton("Settings")

    stop_button.setEnabled(False)

    layout.addStretch()

    layout.addWidget(title, alignment=Qt.AlignCenter)
    layout.addWidget(status, alignment=Qt.AlignCenter)

    layout.addSpacing(20)

    layout.addWidget(start_button)
    layout.addWidget(stop_button)

    buttons_layout = QHBoxLayout()
    buttons_layout.setSpacing(10)

    buttons_layout.addWidget(history_button)
    buttons_layout.addWidget(settings_button)

    layout.addLayout(buttons_layout)

    layout.addStretch()

    history_page = QWidget()
    history_layout = QVBoxLayout(history_page)

    back_button = QPushButton("Back")
    history_title = QLabel("History")
    history_title.setObjectName("pageTitle")
    history_list = QListWidget()

    history_layout.addWidget(back_button)
    history_layout.addWidget(history_title)
    history_layout.addWidget(history_list)

    settings_page = QWidget()
    settings_layout = QVBoxLayout(settings_page)

    settings_layout.setContentsMargins(35, 25, 35, 25)
    settings_layout.setSpacing(10)

    settings_back_button = QPushButton("Back")

    settings_title = QLabel("Settings")
    settings_title.setObjectName("pageTitle")

    settings_layout.addWidget(settings_back_button)
    settings_layout.addWidget(settings_title)
    settings_layout.addSpacing(15)

    general_label = QLabel("GENERAL")
    general_label.setObjectName("sectionTitle")

    folder_label = QLabel("Watched folder:")

    folder_input = QLineEdit()
    folder_input.setText("watched")

    choose_folder_button = QPushButton("Choose folder")

    folder_layout = QHBoxLayout()
    folder_layout.addWidget(folder_input)
    folder_layout.addWidget(choose_folder_button)

    settings_layout.addWidget(general_label)
    settings_layout.addWidget(folder_label)
    settings_layout.addLayout(folder_layout)

    settings_layout.addSpacing(15)

    ai_label = QLabel("AI")
    ai_label.setObjectName("sectionTitle")

    api_key_label = QLabel("Gemini API Key:")

    api_key_input = QLineEdit()
    api_key_input.setEchoMode(QLineEdit.Password)
    api_key_input.setPlaceholderText(
        "Enter your Gemini API key"
    )

    settings_layout.addWidget(ai_label)
    settings_layout.addWidget(api_key_label)
    settings_layout.addWidget(api_key_input)

    settings_layout.addSpacing(15)

    sorting_label = QLabel("AI SORTING")
    sorting_label.setObjectName("sectionTitle")

    sort_checkbox = QCheckBox("Sort files into AI folders")
    sort_checkbox.setChecked(False)

    folders_label = QLabel("Available folders:")

    folders_list = QListWidget()

    new_folder_input = QLineEdit()
    new_folder_input.setPlaceholderText("New folder name")

    add_folder_button = QPushButton("Add")
    remove_folder_button = QPushButton("Remove")

    folder_buttons_layout = QHBoxLayout()
    folder_buttons_layout.addWidget(new_folder_input)
    folder_buttons_layout.addWidget(add_folder_button)
    folder_buttons_layout.addWidget(remove_folder_button)

    settings_layout.addWidget(sorting_label)
    settings_layout.addWidget(sort_checkbox)
    settings_layout.addWidget(folders_label)
    settings_layout.addWidget(folders_list)
    settings_layout.addLayout(folder_buttons_layout)

    settings_layout.addStretch()

    save_setting_button = QPushButton("Save")
    save_setting_button.setObjectName("saveButton")

    settings_layout.addWidget(save_setting_button)

    def choose_folder():
        folder = QFileDialog.getExistingDirectory(
            window,
            "Choose folder"
        )

        if folder:
            folder_input.setText(folder)

    def load_settings():
        try:
            with open(
                "data/config.json",
                "r",
                encoding="utf-8"
            ) as file:
                config = json.load(file)

            folder_input.setText(
                config.get("watch_folder", "watched")
            )

            sort_checkbox.setChecked(
                config.get("sort_into_folders", False)
            )

            api_key_input.setText(
                config.get("api_key", "")
            )

            folders_list.clear()

            folders = config.get("folders", [])

            for folder in folders:
                folders_list.addItem(folder)

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def add_folder():
        folder = new_folder_input.text().strip()

        if not folder:
            return

        existing_folders = [
            folders_list.item(i).text()
            for i in range(folders_list.count())
        ]

        if folder in existing_folders:
            return

        folders_list.addItem(folder)
        new_folder_input.clear()

    def remove_folder():
        selected = folders_list.currentItem()

        if selected:
            folders_list.takeItem(
                folders_list.row(selected)
            )

    def open_settings():
        load_settings()
        stack.setCurrentWidget(settings_page)

    def save_settings():
        folders = [
            folders_list.item(i).text()
            for i in range(folders_list.count())
        ]

        settings = {
            "watch_folder": folder_input.text(),
            "sort_into_folders": sort_checkbox.isChecked(),
            "api_key": api_key_input.text(),
            "folders": folders
        }

        os.makedirs("data", exist_ok=True)

        with open(
            "data/config.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(settings, file, indent=4)

        print("Settings saved.")

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

    def show_window():
        window.show()
        window.raise_()
        window.activateWindow()

    def quit_app():
        stop_watching()
        tray.hide()
        app.quit()

    open_action.triggered.connect(show_window)
    start_action.triggered.connect(start)
    stop_action.triggered.connect(stop)
    quit_action.triggered.connect(quit_app)

    def load_history():
        try:
            with open(
                "data/history.json",
                "r",
                encoding="utf-8"
            ) as file:
                history = json.load(file)

            if not history:
                history_list.clear()
                history_list.addItem("History is empty")
                return

            history_list.clear()

            for item in reversed(history):
                text = (
                    f"{item['new_name']}\n"
                    f"From: {item['old_name']}\n"
                    f"Category: {item['folder']}\n"
                    f"{item['time']}"
                )

                history_list.addItem(text)

        except FileNotFoundError:
            history_list.clear()
            history_list.addItem("History is empty.")

        except Exception as e:
            history_list.clear()
            history_list.addItem(str(e))

    def open_history():
        load_history()
        stack.setCurrentWidget(history_page)

    start_button.clicked.connect(start)
    stop_button.clicked.connect(stop)

    history_button.clicked.connect(open_history)
    settings_button.clicked.connect(open_settings)

    back_button.clicked.connect(
        lambda: stack.setCurrentWidget(main_page)
    )

    settings_back_button.clicked.connect(
        lambda: stack.setCurrentWidget(main_page)
    )

    choose_folder_button.clicked.connect(choose_folder)
    save_setting_button.clicked.connect(save_settings)

    add_folder_button.clicked.connect(add_folder)
    remove_folder_button.clicked.connect(remove_folder)

    stack.addWidget(main_page)
    stack.addWidget(history_page)
    stack.addWidget(settings_page)

    window_layout = QVBoxLayout()
    window_layout.addWidget(stack)

    window.setLayout(window_layout)

    window.show()
    app.exec()