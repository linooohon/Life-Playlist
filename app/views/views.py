from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
import collections

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.model.models import Playlist
from app import db, cache
from app.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET




'''
views 負責 url 對應處理
'''
# Make views' Blueprint instance
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# @cache.cached(timeout=60, key_prefix='home') how to do/how it works/why can't use?
@login_required
def home():
    print("/ GET 沒走 cache")
    if request.method == 'POST':

        artist = request.form.get('artist')
        song = request.form.get('song')

        if len(artist) < 1:
            flash("Artist's name can't be blank!", category='error')
        elif len(song) < 1:
            flash("Song's name can't be blank!;", category='error')
        elif len(current_user.playlists) >= 10:
            flash("Life playlist can only has 10 songs!", category='error')
        else:
            new_playlist_item = Playlist(
                artist=artist, song=song, user_id=current_user.id)
            db.session.add(new_playlist_item)
            db.session.commit()
            flash('your love is added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-playlist-item', methods=['POST'])
# @cache.cached(timeout=60, key_prefix='delete_playlist_item') how to do/how it works/why can't use?
def delete_playlist_item():
    print("/delete-playlist-item POST 沒走 cache")
    playlist_item = json.loads(request.data)
    playlist_item_id = playlist_item['playlistItemId']
    playlist_item = Playlist.query.get(playlist_item_id)
    if playlist_item:
        if playlist_item.user_id == current_user.id:
            db.session.delete(playlist_item)
            db.session.commit()

    return jsonify({})


@views.route('/dashboard', methods=['GET'])
def dashboard():
    all_playlist = Playlist.query.all()
    # for idx, track in enumerate(r['tracks']['items']):
    #     print(idx, track['name'], track['uri']) # uri 可以開啟 spotify 播到那首歌

    # lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
    # results = sp.artist_top_tracks(lz_uri)
    # for track in results['tracks'][:10]:
    #     print('track    : ' + track['name'])
    #     print('audio    : ' + track['preview_url'])  #這個可以聽30秒
    #     print('cover art: ' + track['album']['images'][0]['url'])
    #     print()
    # results = sp.search(q='weezer', limit=20)
    # print(results)

    count_songs_preset_list = []
    dashboard_top10_list = []
    for i in all_playlist:
        whole_name = i.artist + i.song
        whole_name_list = whole_name.lower().strip().split()
        whole_name_string = ''.join(whole_name_list)
        count_songs_preset_list.append(whole_name_string)
        playlist_tupleList = collections.Counter(
            count_songs_preset_list).most_common(10)

    for i in range(0, len(all_playlist)):
        for j in range(0, len(playlist_tupleList)):
            if ''.join((all_playlist[i].artist + all_playlist[i].song).lower().strip().split()) == playlist_tupleList[j][0]:
                dashboard_top10_list.append(all_playlist[i])

    final_pre_list = []
    final_lower_list = []
    final_list = []
    for i in dashboard_top10_list:
        i.artist = i.artist.strip()
        i.song = i.song.strip()
        final_pre_list.append(i)
    for i in final_pre_list:
        if ''.join((i.artist + i.song).lower().strip().split()) not in final_lower_list:
            final_lower_list.append(
                ''.join((i.artist + i.song).lower().strip().split()))
            final_list.append(i)

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
    
    # spotify_artistpage = []
    for i in final_list:
        r = sp.search(q=i.artist, limit=3, type='artist')
        id = r['artists']['items'][0]['id']
        uri = f"spotify:artist:{id}"
        i.uri = uri
        # spotify_artistpage.append(uri)
        print(r['artists']['items'][0]['id'])

    return render_template("dashboard.html", playlists=final_list, user=current_user)
