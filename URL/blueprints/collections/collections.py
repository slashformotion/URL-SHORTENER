from URL.db.models import Collection
from flask import Blueprint, render_template, redirect, url_for, request
from URL.db import db, models
from flask_security import login_required
from flask_login import current_user
from . import forms


collections_bp = Blueprint("collections", __name__, template_folder="templates")


@collections_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = forms.CreateCollection()

    context = {"form": form}
    if request.method == "GET":
        return render_template("collections/create.html", **context)

    elif request.method == "POST" and form.validate_on_submit():
        previous_collections = models.Link.query.filter_by(owner=current_user).all()

        if form.name.data in [col.name for col in previous_collections]:
            context["errors"].append("You have already created this collection.")
            return render_template("collections/create.html", **context)

        else:
            new_col = models.Collection(name=form.name.data, owner=current_user)
            db.session.add(new_col)
            db.session.commit()
            new_id = models.Collection.query.filter_by(name=form.name.data).first().id
            return redirect(url_for("links.dashboard", id=new_id))

    else:
        raise RuntimeError(f"This method <{request.method}> is not usable here.")
