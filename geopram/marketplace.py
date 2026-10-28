"""Marketplace domain validation."""
MARKET_COLLECTIONS=("products","orders","inventory","suppliers","payments","tickets")
def validate_product(record):
    if not record.get("name") and not record.get("product_name"): raise ValueError("Product name is required")
    if float(record.get("price",0)) < 0: raise ValueError("Price cannot be negative")
    return {**record,"currency":record.get("currency","KES"),"status":record.get("status","active")}
