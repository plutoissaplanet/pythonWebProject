import base64
import io


from pandas.core import series

from app import db, ListOfSubs, app, User, Subs
import pandas as pd
import numpy as np
import calplot
from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')

netflix = ListOfSubs(name='Netflix', logo_url="static/Photos/SubsIcons/netflix.png")
spotify = ListOfSubs(name="Spotify", logo_url="static/Photos/SubsIcons/spotify.png")
amazon = ListOfSubs(name="Amazon Prime", logo_url="")
hulu = ListOfSubs(name="Hulu", logo_url="")
youtube = ListOfSubs(name="YouTube", logo_url="")




with app.app_context():


    # if not check_if_exists(netflix):
    #     db.session.add(netflix)
    # if not check_if_exists(spotify):
    #     db.session.add(spotify)
    # if not check_if_exists(amazon):
    #     db.session.add(amazon)
    # if not check_if_exists(hulu):
    #     db.session.add(hulu)
    # if not check_if_exists(youtube):
    #     db.session.add(youtube)
    #
    db.session.commit()
