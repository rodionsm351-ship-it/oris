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

)

app = QApplication(sys.argv)

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.count = 0

        self.setWindowTitle("Трекер задач")
        self.resize(600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        task_layout = QHBoxLayout()
        task_label = QLabel("Task")
        self.task_edit = QLineEdit()
        task_layout.addWidget(task_label)
        task_layout.addWidget(self.task_edit)


        description_label = QLabel("Description")
        self.description_field = QTextEdit()


        button_layout = QHBoxLayout()
        priority_label = QLabel("Priority: ")
        self.low_button = QRadioButton("Low")
        self.medium_button = QRadioButton("Medium")
        self.high_button = QRadioButton("High")

        self.low_button.setChecked(True)

        button_layout.addWidget(priority_label)
        button_layout.addWidget(self.low_button)
        button_layout.addWidget(self.medium_button)
        button_layout.addWidget(self.high_button)


        settings_layout = QHBoxLayout()
        settings_label = QLabel("Parametrs")
        self.important_check = QCheckBox("Important")
        self.favorite_check = QCheckBox("Add to favourite")

        settings_layout.addWidget(settings_label)
        settings_layout.addWidget(self.important_check)
        settings_layout.addWidget(self.favorite_check)

        create_button = QPushButton("Create task")
        clean_button = QPushButton("Clear the form")

        cur_task_label = QLabel("Created task")
        self.cur_task_field = QTextEdit()

        self.result_label = QLabel(f"Your tasks ({len(self.tasks)})")
        self.result_field = QTextEdit()

        delete_button = QPushButton("Delete last task")


        main_layout.addLayout(task_layout)
        main_layout.addWidget(description_label)
        main_layout.addWidget(self.description_field)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(settings_layout)
        main_layout.addWidget(create_button)
        main_layout.addWidget(clean_button)
        main_layout.addWidget(cur_task_label)
        main_layout.addWidget(self.cur_task_field)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.result_field)
        main_layout.addWidget(delete_button)
        

        create_button.clicked.connect(self.create_task)
        create_button.clicked.connect(self.show_tasks)
        clean_button.clicked.connect(self.clear_form)
        delete_button.clicked.connect(self.delete_last_task)


    def create_task(self):
        error = self.check_task()
        if error:
            self.cur_task_field.setText(error)
            return
        
        task = self.task_edit.text()
        description = self.description_field.toPlainText()
        priority = "Low"
        other_settings = []

        if self.medium_button.isChecked():
            priority = "Medium"
        elif self.high_button.isChecked():
            priority = "High"

        if self.important_check.isChecked():
            other_settings.append("Important")
        if self.favorite_check.isChecked():
            other_settings.append("Favorite")

        new_task = {"title": task, "description": description, "priority": priority, "important": self.important_check.isChecked(), "favorite": self.favorite_check.isChecked()}
        self.tasks.append(new_task)
        response = f"{task}\n{description}\n{priority}\n{other_settings}"
        self.cur_task_field.setText(response)


    def check_task(self):
        if self.task_edit.text().strip() == '':
            return "Enter the task"
        if len(self.description_field.toPlainText()) > 200:
            return "Description is too long"
        return


    def show_tasks(self):
        lines = []
        for idx, task in enumerate(self.tasks, start=1):
            importance = "(important)" if task["important"] else " "
            favorite = "*" if task["favorite"] == True else " "
            lines.append(f"{idx}. {task['title']} [{task['priority']}] {importance} {favorite}")
        response = "\n".join(lines)
        
        self.result_field.setText(response)
        self.result_label.setText(f"Your tasks ({len(self.tasks)})")


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


window = TaskManager()
window.show()
sys.exit(app.exec())