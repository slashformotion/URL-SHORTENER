import secrets
from URL import app


def get_new_url():
    return secrets.token_urlsafe(app.config["LENGTH_SHORTEN"])
