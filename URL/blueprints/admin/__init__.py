from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_login import current_user
from flask import request, redirect, url_for
from URL.db import models


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
