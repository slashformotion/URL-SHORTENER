import collections
from flask import Blueprint, render_template, redirect, url_for, request
from URL.db import db, models
from flask_security import login_required
from flask_login import current_user
from . import forms, utils

links_bp = Blueprint("links", __name__, template_folder="templates")


@links_bp.route("/dashboard")
@login_required
def dashboard():
    links = models.Link.query.filter_by(owner=current_user).all()
    collection_id_selected = int(request.args.to_dict().get("collection", 1))
    # print("collection_id_selected:", collection_id_selected)
    # for link in links:
    #     if link.collection.id == collection_id_selected:
    #         print(link, link.collection.id)
    #     else:
    #         print("NOP", link, link.collection.id)
    context = {"links": links, "collection_id_selected": collection_id_selected}
    return render_template("links/dashboard.html", **context)


@links_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = forms.CreateLink()
    form.set_collections(
        models.Collection.query.filter_by(owner=current_user).order_by("name").all()
    )
    context = {"form": form, "errors": []}

    if request.method == "GET":
        return render_template("links/create.html", **context)

    elif request.method == "POST" and form.validate_on_submit():
        previous_links = models.Link.query.filter_by(owner=current_user).all()

        if form.base.data in [link.base for link in previous_links]:
            context["errors"].append("You have already created this link.")
            return render_template("links/create.html", **context)

        else:
            new_shorten = utils.get_new_url()
            previous_shorten = [link.shorten for link in models.Link.query.all()]

            while new_shorten in previous_shorten:
                new_shorten = utils.get_new_url()

            new_link = models.Link(
                base=form.base.data,
                shorten=new_shorten,
                name=form.name.data,
                owner=current_user,
                collection=models.Collection()
                .query.filter_by(id=form.collections.data)
                .first(),
            )
            db.session.add(new_link)
            db.session.commit()
            new_id = models.Link.query.filter_by(base=form.base.data).first().id
            return redirect(url_for("links.infos", id=new_id))


@links_bp.route("/infos/<int:id>")
@login_required
def infos(id):
    link = models.Link.query.filter_by(id=id).first()
    context = {"link": link, "current_user": current_user}
    return render_template("links/link.html", **context)
