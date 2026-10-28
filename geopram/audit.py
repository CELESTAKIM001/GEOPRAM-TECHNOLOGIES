"""Audit event structure helper."""
from datetime import datetime, timezone
def event(name, actor="system", **details): return {"event":name,"actor":actor,"details":details,"at":datetime.now(timezone.utc).isoformat()}
