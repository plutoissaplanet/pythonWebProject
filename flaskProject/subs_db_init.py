from app import db, ListOfSubs, app, delete, User

netflix = ListOfSubs(name='Netflix', logo_url="static/Photos/SubsIcons/netflix.png")
spotify = ListOfSubs(name="Spotify", logo_url="static/Photos/SubsIcons/spotify.png")
amazon = ListOfSubs(name="Amazon Prime", logo_url="")
hulu = ListOfSubs(name="Hulu", logo_url="")
youtube = ListOfSubs(name="YouTube", logo_url="")


def check_if_exists(data):
    subs = ListOfSubs.query.filter_by(name = data.name).first()
    return subs is not None


with app.app_context():
    usersubs = User.query.all()
    for i in usersubs:
        for j in i.subscriptions:
            print("user subs: ", j.name)

    subs=ListOfSubs.query.all()
    for i in subs:
        print(i.name)


    if not check_if_exists(netflix):
        db.session.add(netflix)
    if not check_if_exists(spotify):
        db.session.add(spotify)
    if not check_if_exists(amazon):
        db.session.add(amazon)
    if not check_if_exists(hulu):
        db.session.add(hulu)
    if not check_if_exists(youtube):
        db.session.add(youtube)

    db.session.commit()





