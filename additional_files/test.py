import re
import string


def check_mail(mail):
    errors = []
    if '@' not in mail:
        errors.append(f"{len(errors) + 1}) Знак '@' отсутвует\n")
    if '+' in mail:
        errors.append(f"{len(errors) + 1}) В вашей почте есть '+', что не подходит стандартам\n")
    if errors:
        return errors
    return 'ok'


def check_password(password):
    length_error = 'ok'
    if len(password) < 8:
        length_error = f'Длина пароля должна быть больше 8 символов'

    digit_error = 'ok'
    if not re.findall(r'\d', password):
        digit_error = f'В пароле должна быть хотя-бы одна цифра'
    uppercase_error = 'ok'
    if not re.findall(r'[A-Z]', password):
        uppercase_error = f'В пароле должна быть хотя-бы одна прописная буква'
    lowercase_error = 'ok'
    if not re.findall(r'[a-z]', password):
        lowercase_error = f'В пароле должна быть хотя-бы одна строчная буква'
    return [length_error, digit_error, uppercase_error, lowercase_error]


def check_name_surname(name):
    incorrect = set(name)
    for i in incorrect:
        if i in '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~1234567890''':
            return False
    return True


def split_function(string):
    words = string.split()  # Разделяем строку на слова
    max_length = 62
    lines = []  # Список для хранения строчек
    current_line = ""  # Текущая строчка

    for word in words:
        if len(current_line) + len(
                word) + 1 <= max_length:  # Если текущая строчка + слово + пробел вмещаются в максимальную длину
            current_line += word + " "  # Добавляем слово и пробел к текущей строчке
        else:
            lines.append(current_line)  # Добавляем текущую строчку в список
            current_line = word + " "  # Создаем новую строчку с текущим словом и пробелом

    lines.append(current_line)  # Добавляем последнюю строчку в список
    let = len(lines)
    return lines + [' '] * (5 - let)
