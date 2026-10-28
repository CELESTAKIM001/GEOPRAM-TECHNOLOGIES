# Applying the M-Pesa Till Number patch

This ZIP contains only the affected files, with their original project paths. Extract it into the project root and allow it to overwrite the matching files. Review the resulting changes before committing.

Files included:
- `.env.example` — documents the missing Till Number and the Daraja variables.
- `app.py` — updates the admin Daraja configuration tester to read the new `MPESA_*` names (while supporting legacy aliases).
- `geopram/communications.py` — reports whether Till Number and shortcode settings are configured.
- `modules/daraja_payments.md` — documents the difference between Till Number and Daraja shortcode.
- `README_DEPLOYMENT.md` — adds deployment configuration guidance.

After applying, set the values in Vercel Environment Variables and redeploy. Do not add actual credentials to this ZIP or to Git. This patch does not itself implement live M-Pesa payments.
