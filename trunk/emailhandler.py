import email
import imaplib

from PyQt5 import QtWidgets
import re


def get_first_text_block(email_message_instance):
    """Метод, который возвращает тело письма

    :param email_message_instance: Письмо
    :return: Тело письма
    """

    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                text = part.get_payload(decode=True).decode("utf-8")#.replace('<br>', '\n')
                text = re.sub(r'\<[^>]*\>', '\n', text)
                while len(text) > 0 and len(text.split('\n')) > 0 and len(re.findall(r'\S', text.split('\n')[0])) == 0:
                    text = '\n'.join(text.split('\n')[1:])
                return text
    elif maintype == 'text':
        text = email_message_instance.get_payload(decode=True).decode("utf-8")#.replace('<br>', '\n')
        text = re.sub(r'\<[^>]*\>', '\n', text)
        while len(text) > 0 and len(text.split('\n')) > 0 and len(re.findall(r'\S', text.split('\n')[0])) == 0:
            text = '\n'.join(text.split('\n')[1:])
        return text



class EmailHandler:
    """Класс EmailHandler для работы с почтовым сервисом

      Основное применение - подключение к почтовому сервису
      rambler и поиск писем по тегу
    """

    def __init__(self, username, ext_password):
        """Инициализация и аутентификация к почтовому сервису

        :param username: Логин
        :param ext_password: Пароль
        """

        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setText('Соединение с почтовым сервисом сброшено. Попробуйте перезапустить программу')
        self.username = username
        self.ext_password = ext_password
        # create an IMAP4 class with SSL
        # self.imap = imaplib.IMAP4_SSL("imap.mail.ru")
        self.imap = imaplib.IMAP4_SSL("imap.rambler.ru", 993)
        self.authenticate()

    def authenticate(self):
        """Метод аутентификации"""

        self.imap.login(self.username, self.ext_password)

    def get_messages(self, tag: str):
        """Основной вызываемый метод для работы. Возвращает список найденных по тегу тел писем

        :param tag: Тег
        :return: Список тел писем
        """

        try:
            self.imap.select("inbox")
        except:
            self.imap = imaplib.IMAP4_SSL("imap.rambler.ru", 993)
            self.authenticate()
            try:
                self.imap.select("inbox")
            except:
                self.error_dialog.show()
                exit(0)
        # print(self.imap.list())
        result, data = self.imap.uid('search', None, '(HEADER Subject "' + tag + '")')

        if result != "OK":  # Херовый запрос
            exit(0)

        uidOfMails = data[0].split()  # ID'шники писем, которые мы нашли по тэгу

        if len(uidOfMails) == 0:  # Письма с тэгом не найдены
            return None

        resultList = []

        for uid in uidOfMails:
            # try:
            result, data = self.imap.uid('fetch', uid, 'RFC822')
            # except:
            #     exit(0)

            if result != "OK":  # Херовый запрос
                exit(0)

            email_message = email.message_from_bytes(data[0][1])

            # print(email_message['To'])
            #
            # print(email.utils.parseaddr(email_message['From'])[1])  # получаем имя отправителя "Yuji Tomita"
            #
            # print(email_message.items())  # Выводит все заголовки.

            # Я не знаю как и почему, но эта дичь работает
            resultList.append(get_first_text_block(email_message))

        return resultList

    def close(self):
        """Метод закрытия соединения с почтовым сервисом"""
        try:
            self.imap.close()
            self.imap.logout()
        except:
            return