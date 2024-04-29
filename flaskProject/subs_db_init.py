from app import db, ListOfSubs, app,  User, Subs

netflix = ListOfSubs(name='Netflix', logo_url="static/Photos/SubsIcons/netflix.png")
spotify = ListOfSubs(name="Spotify", logo_url="static/Photos/SubsIcons/spotify.png")
amazon = ListOfSubs(name="Amazon Prime", logo_url="")
hulu = ListOfSubs(name="Hulu", logo_url="")
youtube = ListOfSubs(name="YouTube", logo_url="")


def check_if_exists(data):
    subs = ListOfSubs.query.filter_by(name = data.name).first()
    return subs is not None




with app.app_context():

    # usersubs = Subs.query.filter_by(user_id=1).all()
    # nr_gaming =0
    # category =[]
    # for subs in usersubs:
    #     category.append(subs.category)
    #     nr_gaming=category.count("Gaming")
    # print(category)
    # print(nr_gaming)

    # subs=ListOfSubs.query.all()
    # for i in subs:
    #     print(i.name)


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





