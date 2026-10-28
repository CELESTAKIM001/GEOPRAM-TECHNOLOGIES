"""SMTP configuration validation."""
import os
def smtp_ready():
    required=("SMTP_HOST","SMTP_USERNAME","SMTP_PASSWORD")
    missing=[key for key in required if not os.getenv(key)]
    return {"ready":not missing,"missing":missing}
