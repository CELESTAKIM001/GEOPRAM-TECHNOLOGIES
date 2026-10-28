"""Data export utility for JSON-safe document values."""
import json
def json_safe(records): return json.loads(json.dumps(records, default=str, ensure_ascii=False))
