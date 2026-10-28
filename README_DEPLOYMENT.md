# Geopram Technologies — deployment guide

## Included
Flask application with admin authentication, MongoDB-backed records/settings, generic school and marketplace collections, database exports (JSON/compressed logical database backup/XML/HTML/CSV/XLSX), JSON import, SMTP email sender, API connection diagnostics, audit logging, maintenance mode, landing-page tagline settings, receipt/certificate print views, and optional Kenya-only access gate. Existing static public-site pages and images are retained.

## Deploy on Vercel
1. Create a MongoDB Atlas database user with read/write access only to this application's database. Add Vercel's required network access rules.
2. Import the project to Vercel and set the Root Directory to this folder.
3. Add all values from `.env.example` to Vercel Environment Variables. Never upload a real `.env` or commit credentials.
4. Set `MONGODB_URI`, `DATABASE_NAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and a random `SESSION_SECRET`. Use a Werkzeug hash for `ADMIN_PASSWORD`; create one with `python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('use-a-long-unique-password'))"`.
5. Deploy and test `/health`, then visit `/login`. Admin dashboard: `/geopram-consoleQWERTYUIOP`.
6. Configure custom domains in Vercel project settings. Domain/subdomain DNS and SSL are managed by your DNS provider/Vercel, not by the app.

## Important operational notes
- Vercel functions are stateless and have execution/time limits. MongoDB is the persistent store; do not write persistent uploads to local disk.
- `KENYA_ONLY_MODE=true` uses Vercel's `x-vercel-ip-country` header. It is disabled by default because proxies and missing headers can create false blocks. Keep admin recovery access in mind before enabling it.
- API tester checks connectivity/credential presence only; it does not certify security or call paid SMS, WhatsApp, Daraja, or payment endpoints. SMS/WhatsApp/Daraja delivery requires a real provider adapter and approved credentials.
- Export supports JSON, XML, HTML, CSV and XLSX. Import currently accepts JSON only, by design; review/convert other formats before importing. Exports are capped at 100,000 documents per collection. Protect exports as sensitive data.
- Maintenance mode and landing tagline are controlled from the admin panel. The current maintenance scope is global; granular per-module maintenance, campaign scheduling, bulk mail, automated SMS/WhatsApp, payment callbacks, and full school workflows need provider-specific implementation and acceptance testing before production use.
- Before production: enable MFA/SSO or add a second factor, use a password manager, rotate any credentials previously shared in chat, test restore from Atlas backups, set rate limiting/WAF, review privacy/consent for student data, and commission a security review.


## SMS and WhatsApp credentials

See `modules/sms_whatsapp_setup.md` for the button-by-button Africa's Talking and Meta setup, required environment variables, Vercel steps, and diagnostics. The admin Verify buttons validate credentials only; they do not send messages.
