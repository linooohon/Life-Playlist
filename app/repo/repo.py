from app import db
from app.model.models import Playlist, Dashboard, User, Soulmate_Record

class Repo():
    def __init__(self, model):
        self.model = model
    
    # def __init__(self, table):
    #     self.table = table
    #     self.model = {
    #         "Playlist": Playlist,
    #         "Dashboard": Dashboard,
    #         "User": User,
    #         "Soulmate_Record": Soulmate_Record
    #     }

    # def choose_model(self):
    #     self.model = self.model[self.table]

    def get_data(self, id):
        # self.choose_model()
        return self.model.query.get(id)
    
    def get_all(self):
        return self.model.query.all()

    def get_all_filter_by(self, filter_dic):
        """
        method(1):
            self.model.query.filter_by(**filter_dic).all()
        method(2):
            my_filters = {'artist':'xxxxx', 'song':'xxxxx'}
            query = session.query(self.model)
            for attr,value in my_filters.iteritems():
                query = query.filter( getattr(self.model,attr)==value )
            results = query.all()
        """
        return self.model.query.filter_by(**filter_dic).all()
    
    # def update_data(self, id, update_dic):
    #     row = self.get_data(id)
    #     row.update(update_dic)
    #     db.session.commit()

    def delete_data(self, id):
        row = self.get_data(id)
        db.session.delete(row)
        db.session.commit()

    def insert_data(self, insert_dic):
        """
        Usage:
            Dic: **Dic
            List: *List
        Link: 
            https://stackoverflow.com/questions/31750441/generalised-insert-into-sqlalchemy-using-dictionary
        Example:
            new_top10_data = Dashboard(
            dashboard_artist=i.artist, dashboard_song=i.song, artist_spotify_uri=i.spotify_uri, artist_spotify_image_url=i.spotify_image_url, song_youtube_url=i.youtube_url, artist_genres=i.genres)
            db.session.add(new_top10_data)
            db.session.commit()
        """
        # self.choose_model()
        new_data = self.model(**insert_dic)
        db.session.add(new_data)
        db.session.commit()
