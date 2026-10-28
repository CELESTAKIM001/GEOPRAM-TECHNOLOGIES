"""Local preflight checks; does not contact third-party APIs."""
import os, sys
required=['MONGODB_URI','DATABASE_NAME','ADMIN_EMAIL','ADMIN_PASSWORD','SESSION_SECRET']
missing=[k for k in required if not os.getenv(k)]
if missing:
 print('Missing environment variables:', ', '.join(missing)); sys.exit(1)
if len(os.getenv('SESSION_SECRET',''))<32: print('SESSION_SECRET should be at least 32 characters'); sys.exit(1)
print('Environment preflight passed. Test /health and login after deployment.')
