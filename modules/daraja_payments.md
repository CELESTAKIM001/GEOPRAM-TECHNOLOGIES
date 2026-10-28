# Daraja / M-Pesa configuration

Configure these environment variables in Vercel Project Settings → Environment Variables (and in a local `.env` for development):

- `MPESA_ENVIRONMENT`: `sandbox` or `production`.
- `MPESA_CONSUMER_KEY` and `MPESA_CONSUMER_SECRET`: issued in the Safaricom Daraja developer portal.
- `MPESA_SHORTCODE`: the shortcode registered for the selected Daraja product. Depending on the product, this may be a PayBill or Till shortcode.
- `MPESA_TILL_NUMBER`: the visible business Till Number, when applicable. This is intentionally separate from `MPESA_SHORTCODE`; do not assume they are interchangeable.
- `MPESA_PASSKEY`: passkey for the relevant Daraja product.
- `MPESA_CALLBACK_URL`: public HTTPS callback endpoint.

The admin API tester checks whether required configuration is present. It does not send a live payment request and does not prove the credentials are valid. A production payment integration still needs the appropriate Daraja API flow, callback validation, idempotency, transaction reconciliation, and end-to-end testing. Never put credentials in source control or share them in chat.
