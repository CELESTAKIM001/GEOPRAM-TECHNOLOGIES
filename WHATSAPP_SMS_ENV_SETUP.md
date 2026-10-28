# WhatsApp, SMS, M-Pesa and email environment setup

This package includes a Flask GET/POST endpoint at `/api/whatsapp/webhook` for Meta WhatsApp webhook verification. Deploy the project before registering the callback in Meta.

## Meta webhook
- Callback URL: `https://geopram-technologies.vercel.app/api/whatsapp/webhook` (change the host if your deployment URL differs).
- Verify token: choose a random secret and set it as `WHATSAPP_VERIFY_TOKEN` in Vercel and the exact same value in Meta.
- `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, and `WHATSAPP_BUSINESS_ACCOUNT_ID` come from Meta WhatsApp API Setup.
- `WHATSAPP_APP_SECRET` comes from Meta App Settings → Basic and is used to validate POST webhook signatures.
- `WHATSAPP_GRAPH_API_VERSION` should be set to a Graph API version currently supported by Meta.
- After changing Vercel environment variables, redeploy.

## SMS
Configure Africa's Talking `SMS_USERNAME` and `SMS_API_KEY`; use `SMS_ENVIRONMENT=sandbox` for testing and production credentials/environment only after the account is approved.

## M-Pesa
Use `CONSUMER_KEY`, `CONSUMER_SECRET`, `SHORTCODE`, `PASSKEY`, and a publicly reachable HTTPS `CALLBACK_URL` from your Daraja app. `MPESA_TILL_NUMBER` is optional and only used if the code is written to read it; a Till Number does not replace a shortcode/passkey required by an STK Push implementation.

## Security / limitations
- `.env.example` contains placeholders only. Do not paste actual secrets into source code or commit a real `.env` file.
- The webhook route verifies Meta's GET challenge and validates POST signatures if `WHATSAPP_APP_SECRET` is configured. It currently acknowledges incoming events; it does not yet implement business-specific reply logic or persist messages.
- Environment variables alone do not guarantee that outbound WhatsApp/SMS/M-Pesa flows are fully configured; credentials, account permissions, templates, callback endpoints, and application logic are also required.
