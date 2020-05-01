import smtplib
import ssl
import email
import json

from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage


# IDEA: Encrypt email_settings.json

class EmailSender:
    def __init__(self, settings: dict = None):
        """
        @param settings: <dict> can be used to pass custom settings. loads email_settings.json by default
        """

        if settings is not None:
            self.settings = settings
        else:
            self.__load_settings()

    def __load_settings(self):
        """
        loads email_settings.json file
        """
        with open("email_settings.json", 'r') as settings_file:
            self.settings = json.load(settings_file)

    def set_email_body(self, html=None, text=None):
        """
        @param html: <str> path to email html template

        @param text: <str> email in plain-text
        """
        if html is not None and text is not None:

            with open(html, 'r') as _html_file:
                loaded_html = _html_file.read()

            self.message_body_html = [loaded_html, "html"]
            self.message_body_text = [text, "text"]

    def set_attachment(self, filepath):
        """
        sets the attachment to send with the email. use a zip for multiple attachments
        @param filepath: <str> path to the attachment
        """
        self.attachment_filepath = filepath
        with open(filepath, 'rb') as file:
            self.attachment = MIMEBase("application", "octet-stream")
            self.attachment.set_payload(file.read())

    def __prep_message(self):
        self.message = MIMEMultipart()
        self.message['Subject'] = self.settings['subject']
        self.message['From'] = self.settings['sender']
        self.message['To'] = self.settings['receiver']

        # TODO: see if disabling changes anything
        # self.message['Bcc'] = self.settings['receiver']

        self.message.attach(MIMEText(*self.message_body_html))
        self.message.attach(MIMEText(*self.message_body_text))

        encoders.encode_base64(self.attachment)

        self.attachment.add_header(
            "Content-Disposition",
            f"attachment; filename={self.attachment_filepath}"
        )

        self.message.attach(self.attachment)
        self.message = self.message.as_string()

    def send_email(self):
        """
        Use after set_email_body and set_attachment.
        """

        self.__prep_message()

        context = ssl.create_default_context()
        with smtplib.SMTP(self.settings['smtp_server'], self.settings['port']) as server:
            server.starttls(context=context)
            server.login(self.settings['sender'], self.settings['sender_app_pass'])
            server.sendmail(
                self.settings['sender'],
                self.settings['receiver'],
                self.message
                )
