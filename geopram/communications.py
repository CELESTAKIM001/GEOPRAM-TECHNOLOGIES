"""Communication channel configuration checks; never sends messages by itself."""
import os
def channel_status():
    return {"smtp":bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_USERNAME") and os.getenv("SMTP_PASSWORD")),"sms":bool(os.getenv("SMS_API_KEY")),"whatsapp":bool(os.getenv("WHATSAPP_TOKEN")),"daraja":bool(os.getenv("CONSUMER_KEY") and os.getenv("CONSUMER_SECRET"))}
