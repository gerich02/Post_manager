import json
from channels.generic.websocket import WebsocketConsumer
from .models import Login, Message
from .services import fetch_messages
import logging

logger = logging.getLogger(__name__)


class Messages(WebsocketConsumer):
    """Консьюмер для обработки сообщений."""

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        login_id = data.get("login_id")

        if not login_id:
            self.send(
                json.dumps(
                    {
                        "status": "error",
                        "message": "login_id is required"
                    }
                )
            )
            return

        try:
            login = Login.objects.get(id=login_id)
        except Login.DoesNotExist:
            self.send(
                json.dumps(
                    {
                        "status": "error",
                        "message": "Login not found"
                    }
                )
            )
            return

        initial_message_count = Message.objects.filter(owner=login).count()
        self.send(
            json.dumps(
                {
                    "status": "reading",
                    "progress": 10,
                    "initial_message_count": initial_message_count,
                }
            )
        )

        messages = fetch_messages(login)
        total_messages = len(messages)
        logger.debug(f"Total messages fetched: {total_messages}")

        current_message_count = initial_message_count

        for i, msg_data in enumerate(messages):
            message = Message(
                owner=login,
                theme=msg_data["theme"],
                send_date=msg_data["send_date"],
                receipt_date=msg_data["receipt_date"],
                text=msg_data["text"],
                attachments_list=msg_data["attachments_list"],
            )
            message.save()

            current_message_count += 1
            progress = int(
                (
                    (current_message_count - initial_message_count)
                    / total_messages
                ) * 100
            )
            self.send(
                json.dumps(
                    {
                        "status": "loading",
                        "progress": progress,
                        "message_count": current_message_count,
                        "total_messages": total_messages,
                        "message": {
                            "id": message.id,
                            "theme": message.theme,
                            "send_date": message.send_date.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "receipt_date": message.receipt_date.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "text": message.text[:100],
                            "attachments_list": message.attachments_list,
                        },
                    }
                )
            )

        sorted_messages = (
            Message.objects
            .filter(owner=login)
            .order_by("-send_date")
        )

        self.send(
            json.dumps(
                {
                    "status": "loading",
                    "progress": 100,
                    "messages": [
                        {
                            "id": message.id,
                            "theme": message.theme,
                            "send_date": message.send_date.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "receipt_date": message.receipt_date.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "text": message.text[:100],
                            "attachments_list": message.attachments_list,
                        }
                        for message in sorted_messages
                    ],
                    "total_messages": total_messages,
                    "message_count": current_message_count,
                }
            )
        )

        self.send(
            json.dumps(
                {
                    "status": "completed",
                    "progress": 100,
                    "message_count": current_message_count,
                }
            )
        )
