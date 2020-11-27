from flask import Flask
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_security import Security, SQLAlchemyUserDatastore


app = Flask(__name__)


if app.config.get("ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config.get("ENV") == "testing":
    app.config.from_object("config.TestingConfig")
elif app.config.get("ENV") == "development":
    app.config.from_object("config.DevelopmentConfig")

else:
    raise RuntimeError(
        f'WRONG ENV VARIABLE FOR "FLASK_ENV". you put <{app.config.get("ENV")}>'
    )


from URL.db import models, db

db.init_app(app)
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

from URL.blueprints.auth.auth import auth_bp
from URL.blueprints.links.links import links_bp
from URL.blueprints.public.public import public_bp
from URL.blueprints.collections.collections import collections_bp
from URL.blueprints.api.api import api_bp


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(links_bp, url_prefix="/links")
app.register_blueprint(collections_bp, url_prefix="/collections")
app.register_blueprint(public_bp)
app.register_blueprint(api_bp, url_prefix="/api")
from URL import commands


app.cli.add_command(commands.init)
app.cli.add_command(commands.reset)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(
        self,
    ):
        # redirect to login page if user doesn't have access
        return redirect(url_for("sign_in", next=request.url))


admin = Admin(app, name="URL_SHORTENER", template_mode="bootstrap3")
admin.add_view(MyModelView(models.User, db.session))
admin.add_view(MyModelView(models.Link, db.session))
admin.add_view(MyModelView(models.Hit, db.session))
admin.add_view(MyModelView(models.Role, db.session))
