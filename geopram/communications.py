"""Communication channel configuration checks; never sends messages by itself."""
import os

def channel_status():
    daraja_key = os.getenv("MPESA_CONSUMER_KEY") or os.getenv("CONSUMER_KEY")
    daraja_secret = os.getenv("MPESA_CONSUMER_SECRET") or os.getenv("CONSUMER_SECRET")
    return {
        "smtp": bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_USERNAME") and os.getenv("SMTP_PASSWORD")),
        "sms": bool(os.getenv("SMS_API_KEY")),
        "whatsapp": bool(os.getenv("WHATSAPP_TOKEN")),
        "daraja": bool(daraja_key and daraja_secret),
        "mpesa_till_number_configured": bool(os.getenv("MPESA_TILL_NUMBER")),
        "mpesa_shortcode_configured": bool(os.getenv("MPESA_SHORTCODE") or os.getenv("SHORTCODE")),
    }
