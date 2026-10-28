"""Maintenance mode configuration helpers."""
def normalize_notice(enabled=False, message="We are improving our services.", image="", scope="global"):
    if scope not in ("global","admin"): scope="global"
    return {"maintenance_enabled":bool(enabled),"maintenance_message":str(message)[:1000],"maintenance_image":str(image)[:1000],"maintenance_scope":scope}
