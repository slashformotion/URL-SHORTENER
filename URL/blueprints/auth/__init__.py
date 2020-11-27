from URL import app
from flask import redirect, url_for, request
from flask_login import LoginManager


login = LoginManager(app)


@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect(url_for(".sign_in", next=request.url))
