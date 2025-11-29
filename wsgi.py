import os
from app import create_app

config = {"SECRET_KEY": os.environ.get("SECRET_KEY", "dev-secret")}
app = create_app(config)
