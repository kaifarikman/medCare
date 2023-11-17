from additional_files import confident
import smtplib
from email.message import EmailMessage


def create_authentication_password():
    '''Создаём код ауентефикации, длиной 12 символов'''
    from random import choice
    import string
    digits = list(string.digits)
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase)
    symbols = list(string.punctuation)
    combined = digits + uppercase + lowercase + symbols
    lst = [
        choice(digits), choice(lowercase),
        choice(uppercase), choice(symbols)
    ]
    for _ in range(8):
        lst.append(choice(combined))
    return ''.join(lst)


def send_email(mail, mail_code):
    sender = confident.MAIL_ADMIN
    password = confident.MAIL_PASSWORD
    msg = EmailMessage()
    msg['Subject'] = 'Код подтверждения для приложения medCare'
    msg['From'] = sender
    msg['To'] = mail
    html_mail = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
        h1{'{font-size:40px}'}
        h2{'{font-size:28px;font-weight:900}'}
        p{'{font-weight:100}'}
        td{'{vertical-align:top}'}
        #email{'{margin:auto;width:1000px;background-color:#fff}'}
        </style>
    </head>
    <body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
    <div id="email">
        <table role="presentation" width="100%">
            <tr>
                <td bgcolor="#afeab4" align="center" style="color: black;">
                    <h1> Добро пожаловать в приложение medCare!</h1>
                </td>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
            <tr>
                <td>
                    <h2>Уважаемый пользователь medCare,</h2>
                    <p>
                        Благодарим вас за регистрацию в приложение medCare.
                    </p>
                    <p>
                        Вы предоставили следующий адрес электронной почты при регистрации: {mail}.
                    </p>
                    <p>
                        Чтобы завершить процесс регистрации, используйте следующий код безопасности для учетной записи medCare.
                    </p>
                    <p>
                        Код безопасности: {mail_code}
                    </p>
                    <p>
                        Если это не вы, то просто проигнорируйте данное сообщение.
                    </p>
                    <p>
                        С уважением,
                    </p>
                    <p>
                        Служба технической поддержки medCare.
                    </p>
    
                </td>
    
            </tr>
        </table>
    </div>
    </body>
    </html>
    
    '''

    msg.set_content(html_mail, subtype='html')
    with smtplib.SMTP_SSL('smtp.mail.ru', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
