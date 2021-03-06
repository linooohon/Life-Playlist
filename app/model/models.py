from flask_login import UserMixin
from sqlalchemy.sql import func
# from alembic import op
# from sqlalchemy.sql.schema import UniqueConstraint

from app import db


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(500))
    artist_spotify_uri = db.Column(db.String(500))
    artist_spotify_image_url = db.Column(db.String(500))
    song = db.Column(db.String(500))
    artist_genres = db.Column(db.JSON)
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # 拿到當下時間
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 拿使用者 id 當 fk
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 拿使用者 id 當 fk
    test_migrate_col = db.Column(
        db.String(120), nullable=True)  # 預設就是 nullable=True 可以不寫

    def __init__(self, artist, song, user_id):
        self.artist = artist
        self.song = song
        self.user_id = user_id
        # self.artist_genres = artist_genres


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=False)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    playlists = db.relationship('Playlist')
    third_party = db.Column(db.String(150))
    third_party_id = db.Column(db.String(150))
    # playlists = db.relationship('Playlist', backref='user')

    def __init__(self, email, password, third_party, third_party_id):
        self.email = email
        self.password = password
        self.third_party = third_party
        self.third_party_id = third_party_id
        # self.call()
        # op.drop_constraint(self.email)
        # self.first_name = first_name


class Dashboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dashboard_artist = db.Column(db.String(500))
    dashboard_song = db.Column(db.String(500))
    artist_spotify_uri = db.Column(db.String(500))
    artist_spotify_image_url = db.Column(db.String(500))
    artist_genres = db.Column(db.JSON)
    artist_genres_spotify_uri = db.Column(db.JSON)
    song_youtube_url = db.Column(db.String(500))

    def __init__(self, dashboard_artist, dashboard_song, artist_spotify_uri, song_youtube_url, artist_spotify_image_url, artist_genres):
        self.dashboard_artist = dashboard_artist
        self.dashboard_song = dashboard_song
        self.artist_spotify_uri = artist_spotify_uri
        self.song_youtube_url = song_youtube_url
        self.artist_spotify_image_url = artist_spotify_image_url
        self.artist_genres = artist_genres


class Soulmate_Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_email = db.Column(db.String(500))
    soulmate_email = db.Column(db.String(500))
    same_song = db.Column(db.String(500))

    def __init__(self, original_email, soulmate_email, same_song):
        self.original_email = original_email
        self.soulmate_email = soulmate_email
        self.same_song = same_song
