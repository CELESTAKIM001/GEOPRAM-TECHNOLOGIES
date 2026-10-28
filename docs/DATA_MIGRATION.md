# Data migration

Export formats: JSON, compressed database JSON backup (`.database.json.gz`), XML, HTML, CSV and XLSX. For a true BSON/metadata-preserving MongoDB backup, use MongoDB Atlas backup/restore or `mongodump`; the app-level export is a logical data snapshot, not a full native MongoDB dump. Import accepts JSON object maps of collection names to arrays of records. Other formats are export-only intentionally to avoid unsafe parsing or accidental field coercion. Always back up Atlas before a migration and test imports on a staging database.
