from discord_webhook import DiscordWebhook
import os

SUCCESS_WEBHOOK_URL = os.getenv("DISCORD_SUCCESS_WEBHOOK_URL")
FAILURE_WEBHOOK_URL = os.getenv("DISCORD_FAILURE_WEBHOOK_URL")
WALLET_INFO_WEBHOOK_URL = os.getenv("DISCORD_WALLET_INFO_WEBHOOK_URL")
WALLET_TRANSACTION_WEBHOOK_URL = os.getenv("DISCORD_WALLET_TRANSACTION_WEBHOOK_URL")

def send_discord_notification(webhook_url, message):
    try:
        webhook = DiscordWebhook(url=webhook_url, content=message)
        response = webhook.execute()
        return response
    except Exception as e:
        raise ValueError(f"Error sending Discord notification: {e}")

