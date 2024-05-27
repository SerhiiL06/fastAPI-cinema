from fastapi_mail import FastMail

from src.service.email_service import EmailService


class EmailServiceimpl(EmailService):
    def __init__(self, mail_core: FastMail) -> None:
        self.mail = mail_core

    def send_verificated_message(self, address: str):
        return super().send_verificated_message(address)
