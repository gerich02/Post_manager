import imaplib
import email
from email.header import decode_header
from .models import Message
from datetime import datetime


def decode_header_part(header_part):
    """Декодирует заголовок сообщения электронной почты."""
    if header_part is None:
        return ""

    decoded_parts = decode_header(header_part)
    decoded_header = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            try:
                decoded_header += part.decode(encoding or "utf-8", errors="ignore")
            except LookupError:
                print(f"Unknown encoding: {encoding}")
                decoded_header += part.decode("latin-1", errors="ignore")
        else:
            decoded_header += part
    return decoded_header



def fetch_messages(login):
    """Извлекает сообщения из почтового ящика и сохраняет их в базе данных."""

    messages = []

    if "yandex.ru" in login.login:
        mail_server = "imap.yandex.ru"
    elif "gmail.com" in login.login:
        mail_server = "imap.gmail.com"
    elif "mail.ru" in login.login:
        mail_server = "imap.mail.ru"
    else:
        raise ValueError("Unsupported email provider")

    mail = imaplib.IMAP4_SSL(mail_server)
    mail.login(login.login, login.password)
    mail.select("inbox")

    status, messages_ids = mail.search(None, "ALL")
    email_ids = messages_ids[0].split()

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject_header = msg.get("Subject", "")
        try:
            subject = decode_header_part(subject_header)
        except Exception as e:
            print(f"Error decoding subject: {e}")
            subject = "Unknown Subject"

        date_str = msg.get("Date", "")
        try:
            send_date = email.utils.parsedate_to_datetime(date_str)
            if send_date is None:
                send_date = datetime.min
        except Exception as e:
            print(f"Error parsing date: {e}")
            send_date = datetime.min

        receipt_date = datetime.now()

        text = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        text = part.get_payload(decode=True).decode("utf-8")
                    except UnicodeDecodeError:
                        text = part.get_payload(decode=True).decode(
                            "latin-1", errors="ignore"
                        )
                    break
        else:
            try:
                text = msg.get_payload(decode=True).decode("utf-8")
            except UnicodeDecodeError:
                text = (
                    msg.get_payload(decode=True)
                    .decode("latin-1", errors="ignore")
                )

        attachments = []
        for part in msg.walk():
            if part.get_content_disposition() == "attachment":
                filename = part.get_filename()
                if filename:
                    decoded_filename = decode_header_part(filename)
                    attachments.append(decoded_filename)

        exists = Message.objects.filter(
            owner=login, send_date=send_date, theme=subject
        ).exists()

        if not exists:
            Message.objects.create(
                owner=login,
                send_date=send_date,
                theme=subject,
                receipt_date=receipt_date,
                text=text.replace('\x00', ''),
                attachments_list=", ".join(attachments),
            )

    mail.logout()
    return messages
