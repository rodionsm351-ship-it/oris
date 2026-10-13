import sys

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Профиль пользователя")
window.resize(400, 600)

#----
name_label = QLabel("Имя:")
name_edit = QLineEdit()

layout = QHBoxLayout()
layout.addWidget(name_label)
layout.addWidget(name_edit)

#----
age_label = QLabel("Возраст:")
age_edit = QLineEdit()

age_layout = QHBoxLayout()
age_layout.addWidget(age_label)
age_layout.addWidget(age_edit)

#--
prof_label = QLabel("Профессия:")
prof_edit = QLineEdit()

prof_layout = QHBoxLayout()
prof_layout.addWidget(prof_label)
prof_layout.addWidget(prof_edit)

#----
work_label = QLabel("Формат работы:")
work_layout = QHBoxLayout()

office_rb = QRadioButton("Офис")
remote_rb = QRadioButton("Удаленка")
hybrid_rb = QRadioButton("Гибрид")

work_layout.addWidget(office_rb)
work_layout.addWidget(remote_rb)
work_layout.addWidget(hybrid_rb)

#----
notif_cb = QCheckBox("Получать уведомления")

#---
about_label = QLabel("О себе / Интересы:")
about_edit = QTextEdit()

#---
btn = QPushButton("Сформировать профиль")

#---
result_label = QLabel("Результат:")
result_edit = QTextEdit()

#----
main_layout = QVBoxLayout()
main_layout.addLayout(layout)
main_layout.addLayout(age_layout)
main_layout.addLayout(prof_layout)

main_layout.addWidget(work_label)
main_layout.addLayout(work_layout)

main_layout.addWidget(notif_cb)

main_layout.addWidget(about_label)
main_layout.addWidget(about_edit)

main_layout.addWidget(btn)

main_layout.addWidget(result_label)
main_layout.addWidget(result_edit)

window.setLayout(main_layout)


def show_profile():
    name = name_edit.text()
    age = age_edit.text()
    prof = prof_edit.text()

    if not name:
        result_edit.setText("Пожалуйста, введите имя")
        return

    if not age.isdigit() or not (1 <= int(age) <= 150):
        result_edit.setText("Пожалуйста, введите корректный возраст.")
        return

    if office_rb.isChecked():
        work_format = "Офис"
    elif remote_rb.isChecked():
        work_format = "Удаленка"
    elif hybrid_rb.isChecked():
        work_format = "Гибрид"
    else:
        work_format = "Не выбрано"

    notifications = "Yes" if notif_cb.isChecked() else "No"
    about = about_edit.toPlainText()

    profile_info = (
        f"Имя: {name}\n"
        f"Возраст: {age}\n"
        f"Профессия: {prof}\n"
        f"Формат работы: {work_format}\n"
        f"Уведомления: {notifications}\n\n"
        f"О себе:\n{about}"
    )

    result_edit.setText(profile_info)


btn.clicked.connect(show_profile)

window.show()
sys.exit(app.exec())
