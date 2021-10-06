from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Mail, Message
import json
# from threading import Thread
# import sendgrid
# from sendgrid.helpers.mail import *
# from logging import raiseExceptions

from app.model.models import Playlist, Dashboard
from app import db, cache

'''
views 負責 url 對應處理
'''
# Make views' Blueprint instance
views = Blueprint('views', __name__)


@views.route('/app', methods=['GET', 'POST'])
# @cache.cached(timeout=60, key_prefix='home') how to do/how it works/why can't use?
@login_required
def home():
    print("/app GET 沒走 cache")
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


@views.route('/', methods=['GET'])
def intro():
    return render_template("intro.html", user=current_user)