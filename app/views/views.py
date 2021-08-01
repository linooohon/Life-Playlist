from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.model.models import Playlist
from app import db, cache
import json


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
    # return 'hello world'
    if request.method == 'POST':
        artist = request.form.get('artist')
        song = request.form.get('song')

        if len(artist) < 1:
            flash("Artist's name can't be blank!", category='error')
        elif len(song) < 1:
            flash("Song's name can't be blank!;", category='error')
        else:
            new_playlist_item = Playlist(artist=artist, song=song, user_id=current_user.id)
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
    return render_template("dashboard.html", playlists=all_playlist, user=current_user)
