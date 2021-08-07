from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Mail, Message
import json
import collections

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.model.models import Playlist, User
from app import db, cache, mail
from app.settings import MAIL_USERNAME, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, MAIL_USERNAME


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
    check_same_song_lover()
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
    dashboard_top10_list_duplicate = []
    # loop db all playlist, i == each row
    for i in all_playlist:
        whole_name = i.artist + i.song
        # to lower, strip away blank, split() to list make sure no blank
        whole_name_list = whole_name.lower().strip().split()
        whole_name_string = ''.join(whole_name_list)  # list t0 string
        count_songs_preset_list.append(whole_name_string)

        # get top10 most songs to tuple, but here still in lower case and no blank between artist and song
        playlist_tupleList = collections.Counter(
            count_songs_preset_list).most_common(10)

    # get correct artist and correct song which is showed in playlist_tupleList, and append to List, so here is not only 10 items in List, it will be duplicated.
    for i in range(0, len(all_playlist)):
        for j in range(0, len(playlist_tupleList)):
            if ''.join((all_playlist[i].artist + all_playlist[i].song).lower().strip().split()) == playlist_tupleList[j][0]:
                dashboard_top10_list_duplicate.append(all_playlist[i])

    final_pre_list = []
    final_lower_list = []
    final_list = []
    # pre-process, make sure no blank in artist and song
    for i in dashboard_top10_list_duplicate:
        i.artist = i.artist.strip()
        i.song = i.song.strip()
        final_pre_list.append(i)

    # 過濾重複的 item, 所以只要是在小寫清單有的話, 就不再把真正 user 填的字串放到 final_list
    for i in final_pre_list:
        artist_and_song_lowerstring = ''.join(
            (i.artist + i.song).lower().strip().split())
        if artist_and_song_lowerstring not in final_lower_list:
            final_lower_list.append(artist_and_song_lowerstring)
            final_list.append(i)

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

    for i in final_list:
        # find artist(spotify api)
        r = sp.search(q=i.artist, limit=3, type='artist')
        # make spotify uri
        id = r['artists']['items'][0]['id']
        uri = f"spotify:artist:{id}"
        i.uri = uri
        print(r['artists']['items'][0]['id'])

    return render_template("dashboard.html", playlists=final_list, user=current_user)


def check_same_song_lover():
    current_artistsong_lowerstrip_list = []
    duplicate_filter_list = []
    samesong_list = []
    all_user = User.query.all()
    # 找出 current user 的 playlist to lower, strip, split
    for i in current_user.playlists:
        current_artistsong = i.__dict__['artist'] + i.__dict__['song']
        current_artistsong_lowerstrip = ''.join(
            current_artistsong.lower().strip().split())
        current_artistsong_lowerstrip_list.append(
            current_artistsong_lowerstrip)

    # 從 db 找全部 playlist 看有沒有歌出現在現在這個 user 的 playlist
    for i in all_user:
        for j in i.playlists:
            db_artistsong = j.__dict__['artist'] + j.__dict__['song']
            db_artistsong_lowerstrip = ''.join(
                db_artistsong.lower().strip().split())
            if db_artistsong_lowerstrip in current_artistsong_lowerstrip_list and i.id is not current_user.id \
                    and db_artistsong_lowerstrip not in duplicate_filter_list:
                duplicate_filter_list.append(db_artistsong_lowerstrip)
                samesong_list.append(db_artistsong_lowerstrip)
                if len(samesong_list) >= 3:
                # print(i.id)
                # print(i.email)
                    your_soulmate_email = i.email
                    send_mail(current_user.email, your_soulmate_email)


# email setting for sending soulemate's email to user
def send_mail(current_user_email, soulmate_email):
    print("route correct")
    msg_title = 'Talk to your life playlist soulmate'
    msg_recipients = [current_user_email]
    msg_body = f"your life playlist soulmate's email is {soulmate_email}"
    msg = Message(msg_title, sender=MAIL_USERNAME, recipients=msg_recipients)
    msg.body = msg_body
    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'
