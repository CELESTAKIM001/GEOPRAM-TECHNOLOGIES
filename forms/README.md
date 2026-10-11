# Geopram Forms — responsive HTML prototype

A front-end prototype by Geopram Technologies for building surveys, event registration forms, field data collection forms, and quizzes.

## Pages
- `index.html` — landing page using the supplied Geopram logo and professional photo.
- `dashboard.html` — workspace overview and form list.
- `builder.html` — visual form builder, question types, required fields, options, quiz answer keys, theme/status settings, and preview.
- `templates.html` — starter templates for events, feedback, field data, quizzes and research.
- `preview.html?id=FORM_ID` — public-style form preview and response submission.
- `responses.html` — response history and CSV export.
- `settings.html` — local workspace preferences and reset controls.

## Run it
Open `index.html` in a modern browser. No build step is required. For best results, use a simple local web server (for example, VS Code Live Server) so all pages and assets are served consistently.

## Prototype limitations — important
- Forms and submissions are stored in browser `localStorage`; they do not sync between devices or users.
- File selection is demonstrated in the UI, but uploaded files are not sent to cloud storage.
- Starter dashboard response counts are sample/illustrative data. Real demo submissions are shown in the response page.
- This is not a production multi-user service. Before public deployment or collecting sensitive data, add a secure backend/database, authentication and roles, server-side validation, file storage, anti-spam controls, consent and privacy notices, retention/deletion controls, backups, and audit logging.
- For public multi-device responses, replace browser-only storage with an API and database. Never rely on front-end-only validation for exams or sensitive data.

## Suggested next production stack
Frontend: HTML/CSS/JavaScript or React; backend: Flask/FastAPI/Node.js; database: PostgreSQL; object storage for media; authentication and access control; CSV/XLSX/PDF exports; analytics; shareable public URLs.

## Geopram integration (added)
- Sign in with your Geopram username (email) and password. Tutors and the admin can build forms. Learners can open forms.
- Every form has a unique code (GF-XXXX-XXXX). Respondents sign in, then enter the code at open.html.
- Tutor forms need admin approval before the code works. The admin approves in the Forms dashboard or in admin.html > Forms.
- Sample forms use codes GF-DEMO-0001 and GF-DEMO-0003.
- Still browser-only storage: add a backend before real use.
