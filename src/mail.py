from smtplib import SMTP
from email.message import EmailMessage

from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS


def get_email_template_dashboard(recipient_email: str, recipient_name: str, link_token: str)->EmailMessage:
    email = EmailMessage()

    email["Subject"] = "Подтвердите свой email в tooodo"
    email["From"] = SMTP_USER
    email["To"] = recipient_email

    email.set_content(
        '<div>'
        f'<h1>Подвердите свой email в tooodo, {recipient_name}</h1>'
        f'<p style="font-size: 16px; line-height: 1.2">С вашей электронной почты некий'
        f' зарегестрировал аккаунт в <a style="font-weight: bold" href="google.com">tooodo</a>,'
        f' если это вы, перейдите по'
        f'ссылке ниже для подтверждения. В противном случае проигнорируйте это сообщение</p>'
        f'<a style="font-size: 16px; line-height: 1.2" href="{link_token}" target="_blank">{link_token}</a>',
        subtype="html"
    )

    return email


def send_email_confirmation(recipient_email: str, recipient_name: str, link_token: str):
    print("here")
    email = get_email_template_dashboard(recipient_email, recipient_name, link_token)

    with SMTP(SMTP_HOST, SMTP_PORT) as smtp_server:
        smtp_server.starttls()
        smtp_server.login(SMTP_USER, SMTP_PASS)
        smtp_server.send_message(email)

