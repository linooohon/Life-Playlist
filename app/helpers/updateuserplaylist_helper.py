import sys
import collections
import time
import random
# import logging

from datetime import datetime
from threading import current_thread
from youtubesearchpython import VideosSearch

from app import db, sp
from app.model.models import Playlist, Dashboard, User
from app.repo.repo import Repo



def search_on_youtube(artist_and_song):
    videosSearch = VideosSearch(artist_and_song, limit=1)
    if videosSearch.result()['result'] == []:
        return 'None'
    else:
        return 'https://www.youtube.com/watch?v=' + videosSearch.result()['result'][0]['id']


def search_on_spotify(artist):
    r = sp.search(q=artist, limit=3, type='artist')
    print(r)
    if r['artists']['total'] == 0:
        return 'None', 'None', 'None'
    else:
        uri = 'None'
        pic_url = 'None'
        genres = 'None'
        if r['artists']['items'][0]['uri'] != '':
            uri = r['artists']['items'][0]['uri']
        if len(r['artists']['items'][0]['images']) > 0:
            pic_url = r['artists']['items'][0]['images'][0]['url']
        if len(r['artists']['items'][0]['genres']) > 0:
            genres = r['artists']['items'][0]['genres']
        return uri, pic_url, genres


def update_user_playlist(userplaylist_update_logger):
    # logging.basicConfig(
    #     filename="userplaylist_update.log", level=logging.INFO)
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    user_playlists_withnullgenre = User.query.join(Playlist, User.id == Playlist.user_id).filter(
        Playlist.artist_genres == None).limit(100).all()
    current_time = str(datetime.utcnow())
    try:
        for i in user_playlists_withnullgenre:
            for j in i.playlists:
                time.sleep(random.randrange(1, 5))
                j.uri, j.pic_url, j.genres = search_on_spotify(j.artist)

                # update db
                # update_dic = {
                #     "artist_spotify_uri": j.uri,
                #     "artist_spotify_image_url": j.pic_url,
                #     "artist_genres": j.genres
                # }
                # repo = Repo(Playlist)
                # repo.update_data(j.id, update_dic)
                new_update_playlist_row = Playlist.query.get(j.id)
                new_update_playlist_row.artist_spotify_uri = j.uri
                new_update_playlist_row.artist_spotify_image_url = j.pic_url
                new_update_playlist_row.artist_genres = j.genres
                db.session.commit()
                print("update to db success")
                userplaylist_update_logger.info(
                    f"SUCCESS, fetch spotify api, finished updated user playlist -> time: {current_time} / UTC+0")
    except:
        userplaylist_update_logger.info(
            f"FAIL, fetch spotify api, updating user playlist have some problem -> time: {current_time} / UTC+0")
        print("Unexpected error when execute spotify api:",
              sys.exc_info()[0])
