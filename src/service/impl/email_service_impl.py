from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors

from src.service.email_service import EmailService


class EmailServiceimpl(EmailService):
    def __init__(self, mail_core: FastMail) -> None:
        self.mail = mail_core

    async def send_verificated_message(self, address: str):

        msg = MessageSchema(
            recipients=[address],
            subject="Thank for your registration",
            body="U can verify your email later.",
            subtype=MessageType.html,
        )

        try:
            await self.mail.send_message(msg)
        except ConnectionErrors as e:
            print(e)
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Try again later",
            )

    async def send_recovery_code(self, address: str, code: int):
        body = f"Your recovery password code is {code}. His expired after 5 minutes."
        msg = MessageSchema(
            recipients=[address],
            subject="Recovery password message",
            body=body,
            subtype=MessageType.html,
        )

        await self.mail.send_message(msg)
