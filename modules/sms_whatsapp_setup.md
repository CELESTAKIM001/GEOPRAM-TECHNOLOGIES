# SMS and WhatsApp setup (Geopram Technologies)

This patch supports credential diagnostics only. The Verify buttons do not send messages. Sending SMS/WhatsApp campaigns is a separate feature and must be implemented with consent, templates, provider callbacks, and delivery logs before use.

## Africa's Talking SMS

1. Create/sign in to your account at https://account.africastalking.com/.
2. Open your app dashboard. For testing, click **Go To Sandbox App** and use the sandbox key and username. The sandbox username is `sandbox`.
3. In the selected app, open **Settings → API Key**.
4. Enter your password, click **Generate**, and copy the key immediately. A new key may take a few minutes to become usable.
5. For live SMS, create/configure the production app, use its own API key and application username, top up the account as needed, and obtain an approved sender ID/shortcode if required.
6. Add these environment variables locally and in Vercel:

```dotenv
SMS_PROVIDER="africastalking"
SMS_ENVIRONMENT="sandbox"
SMS_USERNAME="sandbox"
SMS_API_KEY="paste-the-key-here"
```

For production, set `SMS_ENVIRONMENT="production"`, `SMS_USERNAME` to the live application username, and `SMS_API_KEY` to the live key. Never mix sandbox username/key with production credentials.

Official help: https://help.africastalking.com/en/articles/1361037-how-do-i-generate-an-api-key and https://help.africastalking.com/en/articles/2249244-what-is-my-username-and-api-key

## Meta WhatsApp Cloud API

1. Sign in at https://developers.facebook.com/ and open **My Apps**. Create an app if needed.
2. Open/add the **WhatsApp** product and select **API Setup** / **Getting Started**.
3. Use the temporary test token for initial testing. Copy the **Phone number ID** and **WhatsApp Business Account ID** shown on that same screen.
4. Add the test recipient to the allowed recipients if Meta asks. To use a real business number, complete the WhatsApp Business onboarding/number verification and use a properly permissioned production token. Temporary tokens expire; do not treat them as permanent production credentials.
5. Add these environment variables:

```dotenv
WHATSAPP_TOKEN="paste-access-token-here"
WHATSAPP_PHONE_NUMBER_ID="paste-phone-number-id-here"
WHATSAPP_BUSINESS_ACCOUNT_ID="paste-business-account-id-here"
WHATSAPP_GRAPH_API_VERSION="v23.0"
```

Set `WHATSAPP_GRAPH_API_VERSION` to a currently supported version offered in Meta's docs/API Setup if `v23.0` is no longer supported.

Official docs: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

## Add variables to Vercel

1. Open https://vercel.com/dashboard and choose the Geopram project.
2. Open **Settings → Environment Variables → Add New**.
3. Add each variable above by exact name. Select the deployment environments you use (Preview for testing; Production for live service).
4. Save, then redeploy the project. Environment variable changes do not update an already-running deployment automatically.
5. Sign in to Geopram admin, open **Communications → Channel diagnostics**, and click **Verify** for SMS and WhatsApp.
6. Read the result. The SMS check verifies Africa's Talking credentials using its account endpoint. The WhatsApp check calls Meta Graph API with the token and phone number ID. Neither check sends a message.

## Troubleshooting

- SMS authentication failure: confirm username and API key are from the same sandbox/live environment. Wait a few minutes after generating a key.
- WhatsApp token error: generate a fresh token and confirm it has WhatsApp permissions and access to the selected business assets.
- Phone number ID error: copy the ID from the same Meta app/business as the token; do not use the display phone number in its place.
- A successful Verify means credentials passed the check; it does not prove a message can be delivered or that billing, sender ID, templates, recipient consent, and production approvals are complete.
- Do not paste tokens into chat, commit `.env`, put secrets in frontend JavaScript, or screenshot them. If a token leaks, revoke/regenerate it.
