# from logging import raiseExceptions
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Mail, Message
# from threading import Thread
import json


from app.model.models import Playlist, User, Dashboard
from app import db, cache, mail, sp
from app.settings import MAIL_USERNAME, MAIL_USERNAME


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
    # fetch_spotify_youtube()
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
    dashboard_data = Dashboard.query.all()
    return render_template("dashboard.html", dashboard_data=dashboard_data, user=current_user)


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
                if len(samesong_list) >= 1:
                    # print(i.id)
                    # print(i.email)
                    your_soulmate_email = i.email
                    your_soulmate_firstname = i.first_name
                    send_mail(current_user.email, your_soulmate_email,
                              your_soulmate_firstname)


# email setting for sending soulemate's email to user
def send_mail(current_user_email, soulmate_email, soulmate_firstname):
    msg_title = 'Talk to your life playlist soulmate'
    msg_recipients = [current_user_email]
    # msg_body = f"your life playlist soulmate's email is {soulmate_email}"
    msg = Message(msg_title, sender=MAIL_USERNAME, recipients=msg_recipients)
    # msg.body = msg_body
    msg.html = render_template(
        'soulmate_mail.html', soulmate_email=soulmate_email, soulmate_firstname=soulmate_firstname)
    mail.send(msg)
    return 'You Send Mail by Flask-Mail Success!!'


@views.route('/intro', methods=['GET'])
def intro():
    return render_template("intro.html", user=current_user)
