import sys

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
)

app = QApplication(sys.argv)


class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []

        self.setWindowTitle("Task Manager")
        self.resize(600, 600)

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
        self.low_button = QRadioButton("Low")
        self.medium_button = QRadioButton("Medium")
        self.high_button = QRadioButton("High")

        self.low_button.setChecked(True)

        button_layout.addWidget(priority_label)
        button_layout.addWidget(self.low_button)
        button_layout.addWidget(self.medium_button)
        button_layout.addWidget(self.high_button)

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
        clear_button = QPushButton("Clear list")

        deleted_buttons_layout.addWidget(delete_last_button)
        deleted_buttons_layout.addWidget(delete_current_button)


        cur_task_label = QLabel("Created task")
        self.cur_task_field = QTextEdit()
        self.cur_task_field.setReadOnly(True)


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

        main_layout.addWidget(cur_task_label)
        main_layout.addWidget(self.cur_task_field)

        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.priority_filter)
        main_layout.addWidget(self.task_list)

        main_layout.addLayout(deleted_buttons_layout)
        main_layout.addWidget(clear_button)


        create_button.clicked.connect(self.create_task)
        create_button.clicked.connect(self.show_tasks)

        clean_button.clicked.connect(self.clear_form)
        delete_last_button.clicked.connect(self.delete_last_task)
        delete_current_button.clicked.connect(self.delete_current_task)
        clear_button.clicked.connect(self.confirm_clear_list)

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
                padding: 8px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #254f9e;
            }
        """)

    def create_task(self):
        error = self.check_task()

        if error:
            QMessageBox.warning(self, "Error", error)
            return

        task = self.task_edit.text().strip()
        description = self.description_field.toPlainText()

        priority = "Low"

        if self.medium_button.isChecked():
            priority = "Medium"
        elif self.high_button.isChecked():
            priority = "High"

        new_task = {
            "title": task,
            "description": description,
            "priority": priority,
            "important": self.important_check.isChecked(),
            "favorite": self.favorite_check.isChecked()
        }

        self.tasks.append(new_task)

        other_settings = []

        if new_task["important"]:
            other_settings.append("Important")

        if new_task["favorite"]:
            other_settings.append("Favorite")

        response = (
            f"{task}\n"
            f"{description}\n"
            f"{priority}\n"
            f"{other_settings}"
        )

        self.cur_task_field.setText(response)


        self.task_edit.clear()
        self.description_field.clear()

        self.low_button.setChecked(True)
        self.important_check.setChecked(False)
        self.favorite_check.setChecked(False)

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
                f"{idx}. {task['title']} "
                f"[{task['priority']}] "
                f"{importance} {favorite}"
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

        self.low_button.setChecked(True)
        self.important_check.setChecked(False)
        self.favorite_check.setChecked(False)

        self.cur_task_field.clear()

    def delete_last_task(self):
        if self.tasks:
            self.tasks.pop()
            self.show_tasks()
            self.cur_task_field.clear()

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
                        f"{self.tasks.index(task) + 1}. {task['title']} "
                        f"[{task['priority']}] "
                        f"{importance} {favorite}"
                    )

                    if task_text == selected_text:
                        self.tasks.remove(task)
                        break
            else:
                return

            self.show_tasks()
            self.cur_task_field.clear()

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
            self.cur_task_field.clear()


window = TaskManager()
window.show()

sys.exit(app.exec())