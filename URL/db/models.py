from sqlalchemy.sql.schema import BLANK_SCHEMA
from URL.db import db
from URL.blueprints.auth import login
from flask_bcrypt import generate_password_hash
import datetime
from flask_security import UserMixin, RoleMixin
import datetime
from collections import Counter, OrderedDict


@login.user_loader
def load_user(user_id):
    return User.get(user_id)


class Collection(db.Model):
    __tablename__ = "collections"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(80))

    links = db.relationship("Link", back_populates="collection")

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Hit(db.Model):
    __tablename__ = "hits"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    date = db.Column(
        db.String, nullable=False, default=datetime.datetime.utcnow().isoformat()
    )

    link_id = db.Column(db.Integer, db.ForeignKey("links.id"), nullable=False)

    def __str__(self) -> str:
        return f"Hit: date({self.date}), link=(name: {self.link.name} - base: {self.link.base} - owner: {self.link.owner.name})"

    def __repr__(self) -> str:
        return str(self)


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    base = db.Column(db.String, nullable=False)
    shorten = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80))
    date = db.Column(
        db.String, nullable=False, default=datetime.datetime.utcnow().isoformat()
    )

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    hits = db.relationship("Hit", backref="link", lazy=True)

    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"))
    collection = db.relationship("Collection", back_populates="links")

    def __str__(self) -> str:
        return f"Link: name({self.name}), base({self.base}), owner({self.owner.name}), shorten({self.shorten}), collection_id({self.collection.id})."

    def __repr__(self) -> str:
        return str(self)

    def print_date(self):
        return datetime.datetime.fromisoformat(self.date).strftime("%d %b, %Y")

    @property
    def hits_frame(self):
        hits = Counter([hit.date for hit in self.hits])
        result = OrderedDict(sorted(hits.items()))
        return dict(result)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())

    links = db.relationship("Link", backref="owner", lazy=True)

    collections = db.relationship("Collection", backref="owner", lazy=True)

    roles = db.relationship(
        "Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic")
    )

    def __str__(self) -> str:
        return f"User: name({self.name}), linksnumber=({len(self.links)}), role=({self.roles})"

    def __repr__(self) -> str:
        return str(self)

    def get_id(self):
        return self.id

    def __init__(self, name, password, email, roles):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password).decode("UTF-8")
        self.roles = roles
        self.active = True
        col = Collection(name="Default")
        self.collections.append(col)


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
