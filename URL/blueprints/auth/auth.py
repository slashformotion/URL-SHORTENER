from flask import Blueprint, request, redirect, url_for, render_template, flash
from URL import app
from . import forms
from sqlalchemy.exc import IntegrityError
from URL.db import models, db
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user, current_user

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@app.login_manager.unauthorized_handler
def unauth_handler():
    return redirect(url_for("auth.sign_in", next=request.url))


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    form = forms.RegistrationForm()
    context = {"form": form}
    if form.validate_on_submit() and request.method == "POST":
        try:
            new_user = models.User(
                name=form.name.data, email=form.email.data, password=form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return render_template(url_for(".sign_up"), **context)
        return redirect(url_for(".sign_in"))
    return render_template("auth/sign-up.html", **context)


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    form = forms.LoginForm()
    context = {"form": form}
    if form.validate_on_submit() and request.method == "POST":
        user_found = models.User.query.filter_by(email=form.email.data).first()
        if user_found:
            authenticated_user = check_password_hash(
                user_found.password, form.password.data
            )
            if authenticated_user:
                login_user(user_found)

                # redirect to next url
                next_url = request.form.get("next")
                if next_url:

                    return redirect(next_url)

                return redirect(url_for("links.dashboard"))
    context = {"form": form}
    return render_template("auth/sign-in.html", **context)


@auth_bp.route("/logout")
def logout():
    logout_user(current_user)
    flash("You have been logged out.", "info")
    return redirect(url_for("public.index"))
