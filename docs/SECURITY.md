# Security operations

- Keep `.env` out of version control and rotate credentials that have been exposed.
- Use a least-privilege Atlas database user, IP/network restrictions, backups and restore tests.
- Configure a long random `SESSION_SECRET`; enable secure cookies on HTTPS.
- Use a Werkzeug hash for `ADMIN_PASSWORD`. Do not reuse a personal password.
- Export files contain private records; restrict downloads and delete local copies securely.
- The country gate is optional and relies on Vercel metadata; do not treat it as identity verification.
- API diagnostics are connectivity checks, not a security audit or penetration test.
