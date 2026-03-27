import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QFileDialog, \
    QMessageBox, QLineEdit
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
# Импорт нужных библиотек

class InputWindow(QWidget):
    def __init__(self):  # основные настройки
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setGeometry(150, 150, 300, 300)

        self.layout = QVBoxLayout()

        self.label_parent = QLabel("Введите ФИО родителя:") # создание полей для ввода
        self.layout.addWidget(self.label_parent)

        self.parent_input = QLineEdit()
        self.layout.addWidget(self.parent_input)

        self.label_child = QLabel("Введите ФИО ребенка:") # создание полей для ввода
        self.layout.addWidget(self.label_child)

        self.child_input = QLineEdit()
        self.layout.addWidget(self.child_input)

        self.label_class = QLabel("Введите класс ребенка:")# создание полей для ввода
        self.layout.addWidget(self.label_class)

        self.class_input = QLineEdit()
        self.layout.addWidget(self.class_input)

        self.label_letter = QLabel("Введите букву класса ребенка:")# создание полей для ввода
        self.layout.addWidget(self.label_letter)

        self.letter_input = QLineEdit()
        self.layout.addWidget(self.letter_input)

        self.label_date_no = QLabel("Введите дату отсутствия:")# создание полей для ввода
        self.layout.addWidget(self.label_date_no)

        self.date_no_input = QLineEdit()
        self.layout.addWidget(self.date_no_input)

        self.label_who = QLabel("Введите кому:")# создание полей для ввода
        self.layout.addWidget(self.label_who)

        self.who_input = QLineEdit()
        self.layout.addWidget(self.who_input)

        self.label_where = QLabel("Введите адрес проживания:")# создание полей для ввода
        self.layout.addWidget(self.label_where)

        self.where_input = QLineEdit()
        self.layout.addWidget(self.where_input)

        self.label_date = QLabel("Дата:") # создание полей для ввода
        self.layout.addWidget(self.label_date)

        self.date_input = QLineEdit()
        self.date_input.setText(datetime.now().strftime("%Y-%m-%d"))  # Автоматическая подстановка сегодняшней даты
        self.layout.addWidget(self.date_input)

        self.save_button = QPushButton("Сохранить") # создание кнопки для сохранения файла, и её коннект с функцией сохранения файла
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        # словарь для хранения данных, которые были введены в настройках
        self.data = {}

        # загрузка данных из файла при запуске
        self.load_from_file()

    settings_saved = pyqtSignal()  # сигнал для уведомления о сохранении настроек, чтобы при ошибке сразу узнать о ней

    def save_data(self):  # сохранение data
        self.data['ФИО родителя'] = self.parent_input.text()
        self.data['ФИО ребенка'] = self.child_input.text()
        self.data['Класс ребенка'] = self.class_input.text()
        self.data['Буква класса ребенка'] = self.letter_input.text()
        self.data['Дата'] = self.date_input.text()
        self.data['Кому'] = self.who_input.text()
        self.data['Проживающей по адресу'] = self.where_input.text()
        self.data['Дата отсутствия'] = self.date_no_input.text()

        self.save_to_file()

        QMessageBox.information(self, "Все хорошо", "Данные успешно сохранены!")

        self.settings_saved.emit()  # отправляем сигнал после сохранения

    def load_from_file(self):
        try:
            with open("settings.data", "r", encoding="utf-8") as file:  # открытие файла с настройками с прошлого использования(если было)
                for line in file:
                    key, value = line.strip().split(":", 1)
                    self.data[key] = value

            # добавляем значение по умолчанию для поля "Кому", если оно отсутствует. Нужно, чтобы упростить жизнь
            if "Кому" not in self.data:
                self.data[
                    "Кому"] = "Директору ГБОУ Лицея №393 Кировского района г. Санкт-Петербурга Титовой Ольге Андреевне"

            print("Настройки загружены из файла settings.data")
        except FileNotFoundError: # создание файла с настройками, если не было открытий приложения раньше
            print("Файл settings.data не найден. Используются значения по умолчанию.")
            # Значения по умолчанию, если файл отсутствует
            self.data = {
                "Кому": "Директору ГБОУ Лицея №393 Кировского района г. Санкт-Петербурга Титовой Ольге Андреевне"
            }
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить настройки: {e}") # если другая ошибка

    def save_to_file(self): # сохранение настроек в файл, чтобы можно было открыть в следующий раз
        try:
            with open("settings.data", "w", encoding="utf-8") as file:
                for key, value in self.data.items():
                    file.write(f"{key}:{value}\n")
            print("Настройки сохранены в файл settings.data")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить настройки в файл: {e}")

    def update_inputs(self):
        # заполняем поля ввода текущими значениями из self.data
        self.parent_input.setText(self.data.get("ФИО родителя", ""))
        self.child_input.setText(self.data.get("ФИО ребенка", ""))
        self.class_input.setText(self.data.get("Класс ребенка", ""))
        self.letter_input.setText(self.data.get("Буква класса ребенка", ""))
        self.date_no_input.setText(self.data.get("Дата отсутствия", ""))
        self.who_input.setText(self.data.get("Кому",
                                             "Директору ГБОУ Лицея №393"
                                             " Кировского района г. Санкт-Петербурга"
                                             " Титовой Ольге Андреевне"))
        self.where_input.setText(self.data.get("Проживающей по адресу", ""))
        self.date_input.setText(self.data.get("Дата", datetime.now().strftime("%Y-%m-%d")))


class StatementApp(QWidget):
    def __init__(self):  # оформление
        super().__init__()

        self.setWindowTitle("Обработчик заявлений")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.template_label = QLabel("Выберите шаблон заявления:")
        self.layout.addWidget(self.template_label)

        self.template_combo = QComboBox()
        self.template_combo.addItems(
            ["Записка про отсутствие", "Записка про уход самостоятельно", "Освобождение от физкультуры"])
        self.layout.addWidget(self.template_combo)

        self.text_edit = QTextEdit() # создание места, где можно писать
        self.layout.addWidget(self.text_edit)

        self.save_button = QPushButton("Сохранить документ")
        self.save_button.clicked.connect(self.save_document)  # создание кнопки
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.template_combo.currentIndexChanged.connect(self.populate_template)

        self.settings_button = QPushButton("Настройки") # создание кнопки
        self.settings_button.clicked.connect(self.settings)
        self.layout.addWidget(self.settings_button)

        self.help_button = QPushButton("Помощь") # создание кнопки
        self.help_button.clicked.connect(self.show_help)
        self.layout.addWidget(self.help_button)

    def show_help(self):
        help_message = (
            "1. Введите необходимые данные в поля в окне настроек.\n"
            "2. Выберите шаблон заявления из выпадающего списка.\n"
            "3. В шаблон автоматически подставляются данные, введенные в настройках.\n"
            "4. Отредактируйте текст в редакторе, если нужно.\n"
            '5. Нажмите кнопку "Сохранить документ", чтобы сохранить файл с заявлением.\n'
            "6. Для повторного открытия настроек нажмите 'Настройки'."
        )
        QMessageBox.information(self, "Помощь", help_message)

    def populate_template(self):
        # получаем текущий выбранный шаблон, чтобы дальше что-то делать с ним
        template = self.template_combo.currentText()

        # данные из словаря input_window.data (если окно настроек уже открывалось)
        data = getattr(self, 'input_window', None)
        if data:
            data = self.input_window.data
        else:
            data = {}

        # шаблоны с подстановкой данных
        if template == "Записка про отсутствие":
            text = """[Кому] \nOт [ФИО родителя] \nПроживающей по адресу: \n[Проживающей по адресу]\n\t\t\t\t\tЗаявление\nМой ребенок, [ФИО ребенка], ученица(-к), [Класс ребенка][Буква класса ребенка] класса, будет отсутствовать в школе [Дата отсутствия] по семейным обстоятельствам. Ответственность за жизнь и здоровье ребенка беру на себя, пропущенный материал обязуемся пройти самостоятельно.\n\n[Дата]"""
        elif template == "Записка про уход самостоятельно":
            text = """[Кому] \nOт [ФИО родителя]\n\t\t\t\t\tЗаявление\nПрошу разрешить моему ребёнку, [ФИО ребенка], ученицы(-ку), [Класс ребенка][Буква класса ребенка] класса, самостоятельно возращаться с олимпиады [Дата отсутствия]. Ответственность за жизнь и здоровье ребенка беру на себя.\n\n[Дата]"""
        elif template == "Освобождение от физкультуры":
            text = """[Кому] \nOт [ФИО родителя]\n\t\t\t\t\tЗаявление\nПрошу освободить моего ребёнка, [ФИО ребенка], ученицу(-ка), [Класс ребенка][Буква класса ребенка] класса, от занятий физкультурой [Дата отсутствия] в связи с плохим самочувствием, с учебной программой ознакомимся самостоятельно.\n\n[Дата]"""
        else:
            text = ""

        # подстановка значений из словаря в шаблон
        text = text.replace("[ФИО родителя]", data.get("ФИО родителя", "[ФИО родителя]"))
        text = text.replace("[ФИО ребенка]", data.get("ФИО ребенка", "[ФИО ребенка]"))
        text = text.replace("[Дата]", data.get("Дата", "[Дата]"))
        text = text.replace("[Кому]", data.get("Кому", "[Кому]"))
        text = text.replace("[Класс ребенка]", data.get("Класс ребенка", "[Класс ребенка]"))
        text = text.replace("[Буква класса ребенка]", data.get("Буква класса ребенка", "[Буква класса ребенка]"))
        text = text.replace("[Проживающей по адресу]", data.get("Проживающей по адресу", "[Проживающей по адресу]"))
        text = text.replace("[Дата отсутствия]", data.get("Дата отсутствия", "[Дата отсутствия]"))

        self.text_edit.setPlainText(text)

    def save_document(self):  # сохранение документа с выравниванием и ограничением по длине строки
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить документ", "",
                                                       "Text Files (*.txt);;All Files (*)")
            if file_name:
                try:
                    # Получаем текст из поля
                    text = self.text_edit.toPlainText()

                    # Устанавливаем максимальную ширину строки
                    max_width = 70
                    lines = text.split("\n")  # Разделяем текст по строкам

                    formatted_lines = []
                    after_title = False  # флаг, чтобы переключиться после "Заявления"

                    for line in lines:
                        # До строки "Заявление" выравниваем по правому краю
                        if not after_title:
                            # Проверяем, если встретили строку "Заявление", начинаем выравнивание по левому краю
                            if line.strip() == "Заявление":
                                formatted_lines.append(line.strip().center(max_width))  # выровнять по центру
                                after_title = True
                            else:
                                # Разбиваем длинные строки на части, но не разрываем слова
                                while len(line) > max_width:
                                    # Ищем точку разрыва на последнем пробеле в пределах max_width
                                    break_point = line.rfind(' ', 0, max_width)
                                    if break_point == -1:  # если нет пробела, обрезаем по max_width
                                        break_point = max_width
                                    # Добавляем строку до точки разрыва, выравнивая по правому краю
                                    formatted_lines.append(line[:break_point].rstrip().rjust(max_width))
                                    line = line[break_point:].lstrip()  # обрабатываем оставшуюся часть

                                # Добавляем оставшуюся строку, выровненную по правому краю
                                formatted_lines.append(line.rstrip().rjust(max_width))
                        else:
                            # После "Заявления" строки должны выравниваться по левому краю
                            while len(line) > max_width:
                                # Разбиваем строку на части, если она длиннее max_width
                                break_point = line.rfind(' ', 0, max_width)
                                if break_point == -1:  # если нет пробела, обрезаем по max_width
                                    break_point = max_width
                                formatted_lines.append(
                                    line[:break_point].ljust(max_width))  # выравнивание по левому краю
                                line = line[break_point:].lstrip()  # обрабатываем оставшуюся часть

                            # Добавляем оставшуюся строку, выровненную по левому краю
                            formatted_lines.append(line.ljust(max_width))

                    # Сохраняем текст в файл
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write("\n".join(formatted_lines))  # Записываем текст в файл

                    QMessageBox.information(self, "Успех", f"Документ успешно сохранен в: {file_name}")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить документ:\n{e}")  # если не сохраняется
        except Exception as e:
            QMessageBox.critical(self, "Ошибка",
                                 f"Произошла ошибка при вызове диалога сохранения:\n{e}")  # если не сохраняется

    def settings(self):
        if not hasattr(self, 'input_window'):  # проверяем, существует ли окно
            self.input_window = InputWindow()
            self.input_window.settings_saved.connect(self.refresh_template)  # обработка сигнала
        self.input_window.update_inputs()  # обновляем поля. Это надо, чтобы при выходе из настроек, они обновились
        self.input_window.show()

    def refresh_template(self):
        self.populate_template()  # обновляем текстовый шаблон


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = StatementApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        # это используется, чтобы увидеть ошибку(если есть). Я использовала, чтобы понимать где ошибка так как в PyQt не всегда легко понять где ошибка
        app = QApplication(sys.argv)
        error_message = traceback.format_exc()
        QMessageBox.critical(None, "Критическая ошибка", f"Программа завершилась с ошибкой:\n{error_message}")