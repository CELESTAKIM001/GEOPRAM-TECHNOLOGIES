"""Database configuration helper; app.py owns the shared Mongo client."""
import os
def database_config():
    return {"database_name": os.getenv("DATABASE_NAME", "GEOPRAMTECHNOLOGIES"), "configured": bool(os.getenv("MONGODB_URI"))}
