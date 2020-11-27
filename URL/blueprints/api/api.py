from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from URL.db import db, models
from flask_security import login_required
from flask_login import current_user
import datetime

api_bp = Blueprint("api", __name__)


@api_bp.route("link-infos", methods=["POST"])
@login_required
def link_infos():
    if request.is_json:
        id = request.json["id"]
        
        link = models.Link.query.filter_by(id=id).first()
        if link == None:
            return jsonify({"error": "blabla"})
        return jsonify(
            {
                "name": link.name,
                "hits": [
                    [
                        datetime.datetime.fromisoformat(dat).strftime("%Y-%m-%d")
                        for dat in link.hits_frame.keys()
                    ],
                    list(link.hits_frame.values()),
                ],
            }
        )
    else:
        return jsonify({"error": "request data is not json"})


@api_bp.route("url-shorten", methods=["POST"])
@login_required
def url_shorten():
    if request.is_json:
        id = request.json["id"]
        link = models.Link.query.filter_by(id=id).first()
        if link == None:
            return jsonify({"error": "blabla"})
        return jsonify(
            {
                "name": link.name,
                "url": request.host_url[:-1]
                    + url_for("public.redirection", shorten=link.shorten),
            }
        )
    else:
        return jsonify({"error": "request data is not json"})
