import sys
import json
import os

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QRadioButton,
    QCheckBox,
    QPushButton,
    QComboBox,
    QListWidget,
    QMessageBox,
    QDialog,
)

app = QApplication(sys.argv)


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []


        self.setWindowTitle("Task Manager")
        self.resize(600, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        task_layout = QHBoxLayout()

        task_label = QLabel("Task")
        self.task_edit = QLineEdit()
        self.char_count_label = QLabel("Symbols: 0")

        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_edit)

        description_label = QLabel("Description")
        self.description_field = QTextEdit()

        button_layout = QHBoxLayout()

        priority_label = QLabel("Priority:")
        self.priority_choice = QComboBox()
        self.priority_choice.addItems(["Low", "Medium", "High"])

        button_layout.addWidget(priority_label)
        button_layout.addWidget(self.priority_choice)

        settings_layout = QHBoxLayout()

        settings_label = QLabel("Parameters")
        self.important_check = QCheckBox("Important")
        self.favorite_check = QCheckBox("Add to favourite")

        settings_layout.addWidget(settings_label)
        settings_layout.addWidget(self.important_check)
        settings_layout.addWidget(self.favorite_check)

        deleted_buttons_layout = QHBoxLayout()

        create_button = QPushButton("Create task")
        clean_button = QPushButton("Clear the form")

        delete_last_button = QPushButton("Delete last task")
        delete_current_button = QPushButton("Delete selected task")
        edit_task_button = QPushButton("Edit selected task")

        clear_button = QPushButton("Clear list")
        about_button = QPushButton("About this project")

        deleted_buttons_layout.addWidget(delete_last_button)
        deleted_buttons_layout.addWidget(delete_current_button)
        deleted_buttons_layout.addWidget(edit_task_button)


        self.result_label = QLabel("Your tasks (0)")
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All", "Low", "Medium", "High"])
        self.task_list = QListWidget()


        main_layout.addLayout(task_layout)
        main_layout.addWidget(self.char_count_label)

        main_layout.addWidget(description_label)
        main_layout.addWidget(self.description_field)

        main_layout.addLayout(button_layout)
        main_layout.addLayout(settings_layout)

        main_layout.addWidget(create_button)
        main_layout.addWidget(clean_button)

        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.priority_filter)
        main_layout.addWidget(self.task_list)

        main_layout.addLayout(deleted_buttons_layout)
        main_layout.addWidget(clear_button)
        main_layout.addWidget(about_button)


        create_button.clicked.connect(self.create_task)
        create_button.clicked.connect(self.show_tasks)

        clean_button.clicked.connect(self.clear_form)
        clear_button.clicked.connect(self.confirm_clear_list)

        delete_last_button.clicked.connect(self.delete_last_task)
        delete_current_button.clicked.connect(self.delete_current_task)
        edit_task_button.clicked.connect(self.edit_task)

        about_button.clicked.connect(self.show_about_window)

        self.task_edit.textChanged.connect(self.update_char_count)
        self.priority_filter.currentTextChanged.connect(self.show_tasks)


        self.setStyleSheet("""
            QMainWindow {
                background-color: #808080;
            }

            QLabel {
                color: #333333;
                font-size: 14px;
            }

            QLineEdit, QTextEdit, QListWidget {
                background-color: black;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 6px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #3366cc;
                color: black;
                border: none;
                border-radius: 5px;
                padding: 3px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #254f9e;
            }
        """)

        self.load_tasks()

    def create_task(self):
        error = self.check_task()

        if error:
            QMessageBox.warning(self, "Error", error)
            return

        task = self.task_edit.text().strip()
        description = self.description_field.toPlainText()

        priority = self.priority_choice.currentText()

        new_task = {
            "title": task,
            "description": description,
            "priority": priority,
            "important": self.important_check.isChecked(),
            "favorite": self.favorite_check.isChecked()
        }

        self.tasks.append(new_task)
        self.save_history()

        # self.clear_form()

    def check_task(self):
        if self.task_edit.text().strip() == "":
            return "Enter the task"

        if len(self.description_field.toPlainText()) > 200:
            return "Description is too long"

        return None

    def show_tasks(self):
        self.task_list.clear()

        selected_priority = self.priority_filter.currentText()

        for idx, task in enumerate(self.tasks, start=1):
            if selected_priority != "All" and task["priority"] != selected_priority:
                continue

            importance = "(important)" if task["important"] else ""
            favorite = "*" if task["favorite"] else ""

            task_text = (
                f"{idx}.\n"
                f"Name: {task['title']}\n"
                f"[{task['priority']}]\n"
                f"{importance} {favorite}\n"
                f"Description: {task['description']}\n"
            )

            self.task_list.addItem(task_text)

        self.result_label.setText(
            f"Your tasks ({self.task_list.count()} / {len(self.tasks)})"
        )

    def update_char_count(self, text):
        self.char_count_label.setText(
            f"Symbols: {len(text)}"
        )

    def clear_form(self):
        self.task_edit.clear()
        self.description_field.clear()

        self.priority_choice.setCurrentIndex(0)
        self.important_check.setChecked(False)
        self.favorite_check.setChecked(False)

    def delete_last_task(self):
        if self.tasks:
            self.tasks.pop()
            self.show_tasks()
            self.save_history()

    def delete_current_task(self):
        selected_row = self.task_list.currentRow()

        if selected_row != -1:
            answer = QMessageBox.warning(
                self, 
                "Delete task",
                "Are you sure you want to delete this task?", 
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
                )
            
            if answer == QMessageBox.StandardButton.Yes:
                selected_text = self.task_list.currentItem().text()

                for task in self.tasks:
                    importance = "(important)" if task["important"] else ""
                    favorite = "*" if task["favorite"] else ""
                    task_text = (
                        f"{self.tasks.index(task) + 1}.\n"
                        f"Name: {task['title']}\n"
                        f"[{task['priority']}]\n"
                        f"{importance} {favorite}\n"
                        f"Description: {task['description']}\n"
                    )

                    if task_text == selected_text:
                        self.tasks.remove(task)
                        break
            else:
                return

            self.save_history()
            self.show_tasks()

    def confirm_clear_list(self):
        answer = QMessageBox.question(
            self,
            "Clear list",
            "Are you sure you want to delete all tasks?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.tasks.clear()
            self.show_tasks()
            self.save_history()

    def show_about_window(self):
        dialog = AboutDialog()
        dialog.exec()

    def save_history(self):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False)

    def load_tasks(self):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

        self.show_tasks()

    def edit_task(self):
        selected_row = self.task_list.currentRow()

        if selected_row != -1:
            selected_text = self.task_list.currentItem().text()
            for task in self.tasks:
                importance = "(important)" if task["important"] else ""
                favorite = "*" if task["favorite"] else ""
                task_text = (
                    f"{self.tasks.index(task) + 1}.\n"
                    f"Name: {task['title']}\n"
                    f"[{task['priority']}]\n"
                    f"{importance} {favorite}\n"
                    f"Description: {task['description']}\n"
                )
                if task_text == selected_text:
                    dialog = EditTaskDialog(task)
                    if dialog.exec():
                        edited_task = dialog.get_task_data()
                        task.update(edited_task)

                        self.save_history()
                        self.show_tasks()
                    break
        else:
            return


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About program")
        self.resize(300, 250)

        main_layout = QVBoxLayout(self)

        title = QLabel("Task Manager")
        description = QLabel("Use this app to conrol and manage your tasks")
        version = QLabel("Version 2.0")

        main_layout.addWidget(title)
        main_layout.addWidget(description)
        main_layout.addWidget(version)

        self.setStyleSheet("""

                    QLabel {
                        color: #FFFFFF;
                        font-size: 24px;
                    }

                """)


class EditTaskDialog(QDialog):
    def __init__(self, task):
        super().__init__()

        self.title = task['title']
        self.description = task['description']
        self.priority = task['priority']
        self.importance = task['important']
        self.favorite = task['favorite']

        self.setWindowTitle("Edit Task")
        self.resize(500,450)

        main_layout = QVBoxLayout(self)

        task_layout = QHBoxLayout()
        title = QLabel("Edit your task")
        task_label = QLabel("Name")
        self.task_edit = QLineEdit()
        self.task_edit.setText(self.title)
        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_edit)

        description_layout = QHBoxLayout()
        description_label = QLabel("Description")
        self.description_edit = QTextEdit()
        self.description_edit.setPlainText(self.description)
        description_layout.addWidget(description_label)
        description_layout.addWidget(self.description_edit)

        self.priority_edit_button = QComboBox()
        self.priority_edit_button.addItems(["Low", "Medium", "High"])
        self.priority_edit_button.setCurrentText(self.priority)

        settings_label = QLabel("Parameters")
        self.important_check = QCheckBox("Important")
        self.favorite_check = QCheckBox("Add to favourite")
        self.important_check.setChecked(self.importance)
        self.favorite_check.setChecked(self.favorite)

        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.save_button = QPushButton("Save")
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)

        self.cancel_button.clicked.connect(self.cancel_edit_task)
        self.save_button.clicked.connect(self.save_edit_task)

        main_layout.addWidget(title)
        main_layout.addLayout(task_layout)
        main_layout.addLayout(description_layout)
        main_layout.addWidget(self.priority_edit_button)
        main_layout.addWidget(settings_label)
        main_layout.addWidget(self.important_check)
        main_layout.addWidget(self.favorite_check)
        main_layout.addLayout(buttons_layout)

    def cancel_edit_task(self):
        self.reject()

    def save_edit_task(self):
        self.accept()

    def get_task_data(self):
        return {
            "title": self.task_edit.text(),
            "description": self.description_edit.toPlainText(),
            "priority": self.priority_edit_button.currentText(),
            "important": self.important_check.isChecked(),
            "favorite": self.favorite_check.isChecked()
        }











window = TaskManager()
window.show()

sys.exit(app.exec())