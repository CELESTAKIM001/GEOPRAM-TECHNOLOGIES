"""Provider diagnostics for Geopram SMS and WhatsApp integrations.

Diagnostics verify credentials/configuration only. They do not send messages.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request


def _request_json(url, headers, timeout=8):
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(64 * 1024).decode("utf-8", "replace")
            try:
                payload = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                payload = {"message": "Provider returned a non-JSON response."}
            return response.status, payload
    except urllib.error.HTTPError as exc:
        # Read only a bounded response; callers never return secrets to the browser.
        raw = exc.read(16 * 1024).decode("utf-8", "replace")
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"message": "Provider returned an HTTP error."}
        return exc.code, payload


def test_sms_credentials():
    """Validate Africa's Talking credentials with its user/account endpoint."""
    api_key = os.getenv("SMS_API_KEY", "").strip()
    username = os.getenv("SMS_USERNAME", "sandbox").strip()
    environment = os.getenv("SMS_ENVIRONMENT", "sandbox").strip().lower()
    if not api_key:
        return False, "SMS_API_KEY is missing. Add it in Vercel Environment Variables."
    if not username:
        return False, "SMS_USERNAME is missing. Use 'sandbox' for sandbox or your live app username."
    if environment not in ("sandbox", "production", "live"):
        return False, "SMS_ENVIRONMENT must be 'sandbox' or 'production'."
    host = "https://api.sandbox.africastalking.com" if environment == "sandbox" else "https://api.africastalking.com"
    query = urllib.parse.urlencode({"username": username})
    try:
        status, payload = _request_json(host + "/version1/user?" + query, {
            "apiKey": api_key,
            "Accept": "application/json",
            "User-Agent": "Geopram-Technologies/1.0",
        })
        if 200 <= status < 300 and not payload.get("errorMessage"):
            return True, f"Africa's Talking accepted the API credentials for username '{username}' ({environment}). No SMS was sent."
        message = payload.get("errorMessage") or payload.get("message") or payload.get("description") or f"Provider returned HTTP {status}."
        if status in (401, 403):
            message = "Authentication failed. Check that the API key and username belong to the same environment (sandbox/live)."
        return False, str(message)[:240]
    except Exception as exc:
        return False, f"Could not reach Africa's Talking. Check network/provider availability. ({type(exc).__name__})"


def test_whatsapp_credentials():
    """Verify a Meta WhatsApp Cloud API token against the configured phone ID."""
    token = os.getenv("WHATSAPP_TOKEN", "").strip()
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
    version = os.getenv("WHATSAPP_GRAPH_API_VERSION", "v23.0").strip()
    if not token:
        return False, "WHATSAPP_TOKEN is missing. Generate an access token in Meta's WhatsApp API Setup."
    if not phone_id:
        return False, "WHATSAPP_PHONE_NUMBER_ID is missing. Copy the Phone number ID from Meta WhatsApp API Setup."
    if not version.startswith("v") or not re_version(version):
        return False, "WHATSAPP_GRAPH_API_VERSION must look like v23.0; use the version shown in Meta's setup/docs."
    url = f"https://graph.facebook.com/{version}/{urllib.parse.quote(phone_id, safe='')}?fields=display_phone_number,verified_name"
    try:
        status, payload = _request_json(url, {
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "User-Agent": "Geopram-Technologies/1.0",
        })
        if 200 <= status < 300 and payload.get("id", phone_id):
            number = payload.get("display_phone_number", "phone number ID verified")
            name = payload.get("verified_name", "")
            detail = f"Meta accepted the token and phone number ID ({number}). No WhatsApp message was sent."
            if name:
                detail += f" Verified name: {name}."
            return True, detail
        error = payload.get("error", {}) if isinstance(payload, dict) else {}
        code = error.get("code")
        message = error.get("message") or f"Meta returned HTTP {status}."
        if code in (190, 102):
            message = "Meta rejected the access token. Generate/refresh a token and check its WhatsApp permissions."
        elif status == 404:
            message = "Phone number ID not found for this token. Copy the Phone number ID from the same Meta app/business."
        return False, str(message)[:240]
    except Exception as exc:
        return False, f"Could not reach Meta Graph API. Check network/provider availability. ({type(exc).__name__})"


def re_version(value):
    parts = value[1:].split(".")
    return len(parts) == 2 and all(part.isdigit() for part in parts)


def channel_status():
    return {
        "smtp": bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_USERNAME") and os.getenv("SMTP_PASSWORD")),
        "sms": bool(os.getenv("SMS_API_KEY") and os.getenv("SMS_USERNAME")),
        "whatsapp": bool(os.getenv("WHATSAPP_TOKEN") and os.getenv("WHATSAPP_PHONE_NUMBER_ID")),
        "daraja": bool(os.getenv("CONSUMER_KEY") and os.getenv("CONSUMER_SECRET")),
    }
