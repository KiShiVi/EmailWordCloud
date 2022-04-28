import imaplib
import email
from email.header import decode_header
import webbrowser
import os


class EmailHandler:
    def __init__(self, username, ext_password):
        self.username = username
        self.ext_password = ext_password
        # create an IMAP4 class with SSL
        self.imap = imaplib.IMAP4_SSL("imap.mail.ru")

    def authenticate(self):
        # authenticate
        self.imap.login(self.username, self.ext_password)

    def get_messages(self):
        global body
        status, messages = self.imap.select("INBOX")
        # print(self.imap.list())
        messages = int(messages[0])

        # Number of mails to get
        N = min(3, messages)

        print("Status: " + status)
        print("Messages Count: " + str(messages))

        for i in range(messages, min(messages - N, 1), -1):
            res, msg = self.imap.fetch(str(i), "RFC822")
            for response in msg:
                if isinstance(response, tuple):
                    # parse email's bytes into msg
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]

                    if isinstance(subject, bytes):
                        # if it's bytes decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]

                    if isinstance(subject, bytes):
                        # if it's bytes decode to str
                        From = From.decode(encoding)

                    print("Subject:", subject)
                    print("From:", From.decode("UTF-8"))

                    # extract content-type of email
                    content_type = msg.get_content_type()

                    print("Content-type" + content_type)

                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts:
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            body = "some error"
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print(body)
                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    foldername = clean_folder(subject)
                                    if not os.path.isdir(foldername):
                                        # make a folder for this message (named after a subject)
                                        os.mkdir(foldername)

                                    filepath = os.path.join(foldername, filename)
                                    # download attachment and save it (binary mode doesn't take encoding arg
                                    open(filepath, "wb").write(part.get_payload(decode=True))
                    else:
                        # get the email body
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            # print only text email parts
                            print(body)

                    # REMOVE it's unnecessary
                    if content_type == "text/html":
                        # if it's a html file, create new and open it in browser
                        foldername = clean_folder(subject)
                        if not os.path.isdir(foldername):
                            # make a folder for this message (named after a subject)
                            os.mkdir(foldername)
                        filename = "index.html"
                        filepath = os.path.join(foldername, filename)
                        # write the file
                        open(filepath, "w", encoding="utf-8").write(body)
                        # open in the default browser
                        webbrowser.open(filepath)
                    print("="*20)

    def close(self):
        self.imap.close()
        self.imap.logout()


def clean_folder(text):
    # Чистый текст для создания папки.
    return "".join(c if c.isalnum() else "_" for c in text)


def check_connection():
    pass

