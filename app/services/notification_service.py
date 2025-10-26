import os
import logging
from twilio.rest import Client
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class NotificationService:
    def __init__(self):
        self.twilio_sid = os.getenv(
            "TWILIO_ACCOUNT_SID", "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        )
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token")
        self.twilio_whatsapp_from = os.getenv(
            "TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886"
        )
        self.twilio_client = Client(self.twilio_sid, self.twilio_token)
        self.slack_token = os.getenv("SLACK_BOT_TOKEN", "xoxb-your-token")
        self.slack_client = WebClient(token=self.slack_token)
        self.sendgrid_api_key = os.getenv("SENDGRID_API_KEY", "SG.xxxxxxxx")
        self.sendgrid_client = SendGridAPIClient(self.sendgrid_api_key)
        self.sendgrid_from_email = "noreply@foodlink.com"

    def send_notification(
        self, channel: str, recipient: str, event_data: dict, ngo_data: dict
    ):
        if channel == "whatsapp":
            self.send_whatsapp(recipient, event_data)
        elif channel == "slack":
            self.send_slack(recipient, event_data, ngo_data)
        elif channel == "email":
            self.send_email(recipient, event_data, ngo_data)
        else:
            raise ValueError(f"Unsupported notification channel: {channel}")

    def _get_whatsapp_template(self, event: dict) -> str:
        return f"*New Food Surplus Alert from FoodLink!*\n\n*Event:* {event['name']}\n*Location:* {event['location_address']}\n*Surplus:* {event['expected_surplus_kg']} kg of {event['surplus_description']}\n*Organizer:* {event['organizer_name']}\n*Contact:* {event['organizer_phone']}\n\nPlease contact the organizer directly to coordinate pickup."

    def send_whatsapp(self, to_number: str, event_data: dict):
        body = self._get_whatsapp_template(event_data)
        try:
            message = self.twilio_client.messages.create(
                from_=self.twilio_whatsapp_from, body=body, to=f"whatsapp:{to_number}"
            )
            logging.info(f"WhatsApp message sent to {to_number}, SID: {message.sid}")
        except Exception as e:
            logging.exception(f"Failed to send WhatsApp to {to_number}: {e}")
            raise

    def _get_slack_template(self, event: dict, ngo: dict) -> list[dict]:
        return [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":bell: New Food Surplus Alert!",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Event:*\n{event['name']}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Distance:*\n{ngo.get('distance', 'N/A'):.2f} miles away",
                    },
                ],
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Location:*\n{event['location_address']}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Surplus:*\n{event['expected_surplus_kg']}kg of {event['surplus_description']}",
                    },
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Organizer:* {event['organizer_name']} | *Contact:* {event['organizer_phone']}",
                },
            },
            {"type": "divider"},
        ]

    def send_slack(self, channel_id: str, event_data: dict, ngo_data: dict):
        blocks = self._get_slack_template(event_data, ngo_data)
        try:
            self.slack_client.chat_postMessage(
                channel=channel_id, text="New Food Surplus Alert!", blocks=blocks
            )
            logging.info(f"Slack message sent to channel {channel_id}")
        except SlackApiError as e:
            logging.exception(
                f"Failed to send Slack message to {channel_id}: {e.response['error']}"
            )
            raise

    def _get_email_template(self, event: dict, ngo: dict) -> str:
        distance_str = f"{ngo.get('distance', 'N/A'):.2f}"
        return f"<html>\n            <body style='font-family: sans-serif; color: #333;'>\n                <div style='max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;'>\n                    <h1 style='color: #0056b3;'>New Food Surplus Alert from FoodLink!</h1>\n                    <p>A new surplus food opportunity is available near you.</p>\n                    <hr>\n                    <h2>{event['name']}</h2>\n                    <p><strong>Distance:</strong> {distance_str} miles away</p>\n                    <p><strong>Location:</strong> {event['location_address']}</p>\n                    <p><strong>Surplus:</strong> {event['expected_surplus_kg']} kg of {event['surplus_description']}</p>\n                    <hr>\n                    <h3>Organizer Contact</h3>\n                    <p><strong>Name:</strong> {event['organizer_name']}</p>\n                    <p><strong>Phone:</strong> {event['organizer_phone']}</p>\n                    <p>Please contact the organizer directly to coordinate pickup.</p>\n                    <div style='margin-top: 20px; text-align: center; font-size: 12px; color: #888;'>\n                        <p>You received this email because you are registered with FoodLink.</p>\n                    </div>\n                </div>\n            </body>\n            </html>"

    def send_email(self, to_email: str, event_data: dict, ngo_data: dict):
        subject = f"Food Surplus Alert: {event_data['name']}"
        html_content = self._get_email_template(event_data, ngo_data)
        message = Mail(
            from_email=self.sendgrid_from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        try:
            response = self.sendgrid_client.send(message)
            logging.info(
                f"Email sent to {to_email}, status code: {response.status_code}"
            )
        except Exception as e:
            logging.exception(f"Failed to send email to {to_email}: {e}")
            raise