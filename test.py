from URL.db.models import Link, User, Hit, Role, Collection
from URL.db import db
from URL import app
import secrets
import datetime
import random

app.config.from_object("config.DevelopmentConfig")
with app.app_context():
    db.drop_all()
    db.create_all()

    def random_date():

        start_date = datetime.datetime(2020, 1, 1, 10)
        end_date = datetime.datetime(2020, 2, 1, 22)

        time_between_dates = end_date - start_date
        between_dates = time_between_dates.days
        random_number_of_seconds = random.randrange(between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_seconds)
        return random_date.isoformat()

    colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]

    fruits = [
        "Apple",
        "Orange",
        "Grape",
        "Mango",
        "Bananas",
        "Boysenberries",
        "Blueberries",
        "Bing Cherry",
        "Rambutan",
        "Raspberries",
        "Rose Hips",
        "Watermelon",
        "Wolfberry",
        "White Mulberr",
    ]

    def get_fruit():
        return random.choice(fruits)

    def random_number(n):
        return "".join([str(random.randint(0, 9)) for _ in range(n)])

    admin_role = Role(name="admin")
    classic_role = Role(name="classic", description="superawesome classic user")

    user1 = User(
        name="admin", password="12345678", roles=[admin_role], email="admin@email.com"
    )
    user2 = User(
        name="classic",
        password="voilavoila",
        roles=[classic_role],
        email="classic@email.com",
    )

    for i, color in enumerate(colors):
        if i % 2 == 0:
            user = user1
        else:
            user = user2
        col = Collection(name=color, owner=user)
        db.session.add(col)

    print([col.name for col in user2.collections])
    db.session.add(admin_role)
    db.session.add(classic_role)
    db.session.add(user1)
    db.session.add(user2)

    for num in range(1, 5):
        tag = random.choices
        link1 = Link(
            name=get_fruit(),
            base=f"base{num}",
            shorten=secrets.token_urlsafe(5),
            owner=user1,
            collection=random.choice(user1.collections),
        )

        db.session.add(link1)
        # print(link1.collection)
        for num in range(10):
            hit = Hit(date=random_date(), link=link1)
            db.session.add(hit)

    for num in range(20, 50):
        link2 = Link(
            name=get_fruit(),
            base=f"base{num}",
            shorten=secrets.token_urlsafe(5),
            owner=user2,
            collection=random.choice(user2.collections),
        )

        db.session.add(link2)
        for num in range(10):
            hit = Hit(date=random_date(), link=link2)
            db.session.add(hit)

    db.session.commit()
    print(link2.collection.id)
