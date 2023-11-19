from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout,
                             QGraphicsScene)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

import sys
from random import choice
import pandas as pd
from urllib import request

import db
from additional_files import email_sender
from additional_files import test
import for_pharmaciesDB


class CreateCard(QMainWindow):
    def __init__(self, information_of_pill):
        super().__init__()
        self.information_of_pill = information_of_pill
        self.image_path = information_of_pill[1]
        self.title = information_of_pill[0]
        self.price = information_of_pill[2]
        split_title = test.split_function(information_of_pill[0])

        self.new_window = QMainWindow()  # Создаем новое окно

        self.image_label = QLabel()  # Создаем QLabel для изображения
        self.set_image(self.image_path)
        self.title_label1 = QLabel(split_title[0])  # Создаем QLabel
        self.title_label2 = QLabel(split_title[1])  # Создаем QLabel
        self.title_label3 = QLabel(split_title[2])  # Создаем QLabel
        self.title_label4 = QLabel(split_title[3])  # Создаем QLabel
        self.title_label5 = QLabel(split_title[4])  # Создаем QLabel

        self.price_label = QLabel(self.price)  # Создаем QLabel для цены
        self.loyaout = QVBoxLayout(self)
        self.button = QPushButton('Перейти к товару')  # Создаем кнопку
        self.button.setStyleSheet("border-radius:5px;")
        self.loyaout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.button.clicked.connect(
            self.open_window
        )  # Подключаем обработчик сигнала clicked
        self.add_widgets()

    def add_widgets(self):
        # Создаем QVBoxLayout и добавляем QLabel-ы и кнопку в него
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.title_label1)
        layout.addWidget(self.title_label2)
        layout.addWidget(self.title_label3)
        layout.addWidget(self.title_label4)
        layout.addWidget(self.title_label5)
        layout.addWidget(self.price_label)
        layout.addLayout(self.loyaout)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setStyleSheet("background-color:rgb(255,247,232);")
        self.setCentralWidget(widget)

    def set_image(self, image_path):
        '''Данная функция загружает изображение из указанного пути,
        обрабатывает его и устанавливает как картинку для
        виджета image_label'''
        try:
            data = request.urlopen(image_path).read()
        except Exception:
            data = request.urlopen(
                'https://sklad-vlk.ru/d/cml_b29980cb_b3733bd1.jpg'
            ).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(200, 200)
        self.image_label.setPixmap(pixmap)

    def open_window(self):
        uic.loadUi('qt/product.ui', self.new_window)

        product_photo = QGraphicsScene()
        pixmap = QPixmap()
        data = request.urlopen(self.image_path).read()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(250, 250)
        product_photo.addPixmap(pixmap)

        d = eval(self.information_of_pill[6])

        lst = []
        for k, v in d.items():
            for value in v:
                lst.append([k, value])
        random_pharma = lst
        if len(lst) > 5:
            random_pharma = [choice(lst) for _ in range(5)]
        if not random_pharma:
            self.new_window.label_1.setText('аптеки отсутствуют!')
        else:
            index = 0
            count = 1
            while count <= len(random_pharma) * 2:
                first = eval(f'self.new_window.label_{count}')
                second = eval(f'self.new_window.label_{count + 1}')
                f = random_pharma[index]
                first.setText(f[0])
                second.setText(f[1])
                index += 1
                count += 2

        self.new_window.product_cancelButton.clicked.connect(self.cancel)
        self.new_window.product_nameLabel.setText(self.title)
        font = QFont("Arial", 10)
        self.new_window.product_nameLabel.setFont(font)
        self.new_window.product_priceLabel.setText(self.price)
        font_price = QFont("Arial", 10)
        self.new_window.product_priceLabel.setFont(font_price)
        self.new_window.product_photo.setScene(product_photo)
        self.new_window.product_from_whatLabel.setText(
            self.information_of_pill[3]
        )
        font_infplill3 = QFont("Arial", 10)
        self.new_window.product_from_whatLabel.setFont(font_infplill3)
        self.new_window.product_analogLabel.setText(
            self.information_of_pill[4]
        )
        font_pill4 = QFont("Arial", 10)
        self.new_window.product_analogLabel.setFont(font_pill4)
        self.new_window.product_informationLabel.setText(
            self.information_of_pill[5]
        )
        font_pill5 = QFont("Arial", 10)
        self.new_window.product_informationLabel.setFont(font_pill5)

        self.new_window.product_nameLabel.setAlignment(Qt.AlignCenter)
        self.new_window.product_priceLabel.setAlignment(Qt.AlignCenter)
        self.new_window.product_from_whatLabel.setAlignment(Qt.AlignCenter)
        self.new_window.product_analogLabel.setAlignment(Qt.AlignCenter)

        self.new_window.showNormal()  # Отображаем новое окно

    def cancel(self):
        self.new_window.close()


class TryOpen(QWidget):
    def __init__(self, categories, dictionary):
        super().__init__()
        data = list()
        for k, v in dictionary.items():
            if k in categories:
                data.extend(v)
        self.data = data
        self.create_win()

    def create_win(self):
        lst = self.data
        layout = QVBoxLayout()
        n = len(lst)  # всего строчек в csv
        ind = 0
        for _ in range(n // 3):
            row_layout = QHBoxLayout()  # Создаем QHBoxLayout для каждого ряда
            for _ in range(3):
                card = CreateCard(lst[ind])
                row_layout.addWidget(card)  # Добавляем карточку в текущий ряд
                ind += 1
            layout.addLayout(row_layout)  # Добавляем текущий ряд в QVBoxLayout
        widget = QWidget()
        widget.setLayout(layout)
        return widget


class SaveInformation(QWidget):
    def __init__(self):
        super().__init__()
        self.saveInfo()

    def saveInfo(self):
        csv_file = 'parsing/all_products.csv'
        df = pd.read_csv(csv_file, sep=';')
        d = dict()
        # count = 0  # для быстрых тестирований
        for index, row in df.iterrows():
            # if count == 30:  # для быстрых тестирований
            #     break  # для быстрых тестирований
            card = row.tolist()
            if 'https' not in card[1]:
                card[1] = 'https://sklad-vlk.ru/d/cml_b29980cb_b3733bd1.jpg'
            from_what = card[3]
            if d.get(from_what):
                values = d.get(from_what)
                values.append(card)
                d[from_what] = values
            else:
                d[from_what] = [card]
            # count += 1  # для быстрых тестирований
        all_categories = sorted(list(d.keys()))
        return all_categories, d


class PharmacyCard(QWidget):
    def __init__(self, pharmacy):
        super().__init__()
        layout = QHBoxLayout()
        layout.addWidget(QLabel(f"Название: {pharmacy[0]}"))
        layout.addWidget(QLabel(f"Адрес: {pharmacy[1]}"))
        self.setLayout(layout)


class MainApp(QWidget):
    def __init__(self, categories, dictionary):
        super().__init__()
        counter = 20 // len(categories)
        lst = []
        for k, v in dictionary.items():
            values = [choice(v) for _ in range(counter)]
            lst.extend(values)
        self.lst = lst
        self.show_win()

    def show_win(self):
        lst = self.lst
        layout = QVBoxLayout()
        n = len(lst)  # всего строчек в csv
        ind = 0
        for _ in range(n // 3):
            row_layout = QHBoxLayout()  # Создаем QHBoxLayout для каждого ряда
            for _ in range(3):
                card = CreateCard(lst[ind])
                row_layout.addWidget(card)  # Добавляем карточку в текущий ряд
                ind += 1
            layout.addLayout(row_layout)  # Добавляем текущий ряд в QVBoxLayout
        widget = QWidget()
        widget.setLayout(layout)
        return widget


class MedCare(QMainWindow):
    def __init__(self, categories, dictionary, productsUI, main_app):
        super().__init__()
        self.data = []
        self.all_categories, self.d = categories, dictionary
        self.all_productsUI = productsUI
        self.main_appUI = main_app
        self.start()

    def start(self):
        uic.loadUi('qt/initial_window.ui', self)
        self.sign_inButton.clicked.connect(self.sign_in)
        self.sign_upButton.clicked.connect(self.sign_up)

    def sign_in(self):
        login, password = self.check_signing()
        if db.get_user(login, password):
            self.errorLabel.setText(' ')  # нужен вывод на экран
            self.data = db.get_user(login, password)
            self.main_app()
        else:
            self.errorLabel.setText('Неправильный логин или пароль!')

    def check_signing(self):
        login = self.LoginEdit.text()
        password = self.PasswordEdit.text()
        return login, password

    def main_app(self):
        uic.loadUi('qt/main_App.ui', self)
        self.scrollArea.setWidget(self.main_appUI.show_win())
        self.user_profile.clicked.connect(self.user_profile_function)
        self.all_products.clicked.connect(self.all_products_function)
        self.illness.clicked.connect(self.illness_function)
        self.pharmacies.clicked.connect(self.pharmacies_function)
        self.settings.clicked.connect(self.settings_function)
        self.about_application.clicked.connect(self.about_application_function)

    def sign_up(self):
        uic.loadUi('qt/registration.ui', self)
        self.registration_registrationButton.clicked.connect(self.add_user)
        self.registration_backwardButton.clicked.connect(self.start)

    def add_user(self):
        name = self.registration_lineEditName.text()
        surname = self.registration_lineEditSurname.text()
        mail = self.registration_lineEditMail.text()
        password = self.registration_lineEditPassword.text()
        flag = True
        if test.check_mail(mail) != 'ok':
            errors = test.check_mail(mail)
            s = (f'''
            Ваша почта не подходит нашим стандартам:\n{''.join(errors)}'''
                 .strip())
            st = self.registration_errorLabel.text() + s
            self.registration_errorLabel.setText(st)  # нужен вывод на экран
            flag = False

        if len(set(test.check_password(password))) != 1:
            error = '\nПароль неправильный, так как:\n'
            for i in test.check_password(password):
                if i != 'ok':
                    error += f'{i}\n'
            st = self.registration_errorLabel.text() + error
            self.registration_errorLabel.setText(st)  # нужен вывод на экран
            flag = False

        if not name:
            st = self.registration_errorLabel.text() + 'Вы не ввели имя\n'
            self.registration_errorLabel.setText(st)  # нужен вывод на экран
            flag = False

        if not surname:
            st = self.registration_errorLabel.text() + 'Вы не ввели фамилию\n'
            self.registration_errorLabel.setText(st)  # нужен вывод на экран
            flag = False

        if not flag:
            st = (self.registration_errorLabel.text() +
                  '\nВы не можете быть авторизованы в приложение medCare\n')
            self.registration_errorLabel.setText(st)  # нужен вывод на экран
        else:
            uic.loadUi('qt/checker.ui', self)
            self.data = (name, surname, mail, password)
            self.program_code = email_sender.create_authentication_password()
            email_sender.send_email(mail, self.program_code)
            self.checker_register.clicked.connect(self.register)
            self.checker_cancelButton.clicked.connect(self.sign_up)

    def register(self):
        data = self.data
        program_mail_code = self.program_mail_code
        mail_code = self.checker_mailCode.text()
        if mail_code == program_mail_code:
            if db.add_user(data):
                self.start()
            else:
                self.error_label.setText(
                    'Аккаунт на такую почту уже существует. '
                    'Перерегистрируйтесь'
                )
        else:
            self.error_label.setText(
                'Код введен неверно. Зарегистрируйтесь заново!'
            )

    def user_profile_function(self):
        uic.loadUi('qt/profile.ui', self)
        self.profile_backwardButton.clicked.connect(self.main_app)
        self.profile_logoutButton.clicked.connect(self.start)
        name, surname = self.data[0][:2]
        self.profile_usernameLabel.setText(name)
        self.profile_usersurnameLabel.setText(surname)
        self.profile_usertownLabel.setText('Набережные Челны')

    def all_products_function(self):
        uic.loadUi('qt/all_products.ui', self)
        self.scrollproducts.setWidget(self.all_productsUI.create_win())
        self.back.clicked.connect(self.main_app)

    def illness_function(self):
        uic.loadUi('qt/illness.ui', self)
        self.illness_cancelButton.clicked.connect(self.main_app)
        self.illness_categories = list()
        for i in range(1, 9):
            cb = eval(f'self.checkBox_{i}')
            cb.stateChanged.connect(
                lambda state, checkbox=cb: self.add_box(state, checkbox)
            )

        self.illness_findButton.clicked.connect(self.find_categories)

    def add_box(self, state, checkbox):
        if state == 2:
            self.illness_categories.append(checkbox.text())

    def find_categories(self):
        categories = self.illness_categories
        uic.loadUi('qt/all_products.ui', self)
        ui = TryOpen(categories, self.d).create_win()
        self.scrollproducts.setWidget(ui)
        self.back.clicked.connect(self.illness_function)

    def pharmacies_function(self):
        uic.loadUi("qt/pharmacies.ui", self)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        pharmacies = for_pharmaciesDB.all_pharmacies()
        for pharmacy in pharmacies:
            card = PharmacyCard(pharmacy)
            scroll_layout.addWidget(card)

        self.scrollapteki.setWidget(scroll_widget)
        self.back.clicked.connect(self.main_app)

    def settings_function(self):
        uic.loadUi('qt/settings.ui', self)
        self.settings_cancelButton.clicked.connect(self.main_app)
        self.settings_saveButton.clicked.connect(self.update_data)

    def update_data(self):
        new_name = self.settings_nameLine.text()
        new_surname = self.settings_surnameLine.text()
        town = self.settings_townLine.text()
        flag = True
        if not test.check_name_surname(new_name) or new_name == '':
            self.settings_nameErrorLabel.setText('Введите адекватное имя')
            flag = False
        if not test.check_name_surname(new_surname) or new_surname == '':
            self.settings_surnameErrorLabel.setText(
                'Введите адекватную фамилию'
            )
            flag = False
        if town.lower() != 'набережные челны':
            self.settings_townErrorLabel.setText(
                'Данное приложение работает только в г.Набережные Челны.'
            )
            flag = False
        if flag:
            data = self.data
            new_data = [tuple((new_name, new_surname, data[0][2], data[0][3]))]
            self.data = db.change_user(data, new_data)
            self.main_app()

    def about_application_function(self):
        uic.loadUi('qt/about_application.ui', self)
        self.back_intoMain.clicked.connect(self.main_app)


class WiFiError(QMainWindow):
    def __init__(self):
        super().__init__()
        self.open_window()

    def open_window(self):
        uic.loadUi('qt/notwifi.ui', self)


if __name__ == '__main__':
    try:
        request.urlopen("http://google.com")
        db.start_session()
        app = QApplication(sys.argv)
        all_categories, d = SaveInformation().saveInfo()
        all_productsUI = TryOpen(all_categories, d)
        main_appUI = MainApp(all_categories, d)
        ex = MedCare(all_categories, d, all_productsUI, main_appUI)
        ex.show()
        sys.exit(app.exec_())
    except IOError:
        app = QApplication(sys.argv)
        ex = WiFiError()
        ex.show()
        sys.exit(app.exec_())
        
