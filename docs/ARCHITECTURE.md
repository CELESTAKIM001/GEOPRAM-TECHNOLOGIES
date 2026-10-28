# Architecture

`app.py` is the Vercel-compatible Flask entrypoint. MongoDB Atlas is the durable data layer. Jinja templates provide public, admin, maintenance and print views. `geopram/` contains reusable domain helpers; `schemas/` documents common record shapes.
