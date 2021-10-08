from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_user
from flask_mail import Mail, Message
import json
# from threading import Thread
# import sendgrid
# from sendgrid.helpers.mail import *
# from logging import raiseExceptions

from app.model.models import Playlist, Dashboard, User
from app import db, cache
from app.settings import GOOGLE_OAUTH2_CLIENT_ID
from flask_cors import CORS

from google.oauth2 import id_token
import google.auth.transport.requests as google_requests



'''
views 負責 url 對應處理
'''
# Make views' Blueprint instance
views = Blueprint('views', __name__)
CORS(views)

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
            # flash('your love is added!', category='success')

    return render_template("home.html", user=current_user, GOOGLE_OAUTH2_CLIENT_ID=GOOGLE_OAUTH2_CLIENT_ID)


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


# https://developers.google.com/identity/sign-in/web/backend-auth
# https://stackoverflow.com/questions/12909332/how-to-logout-of-an-application-where-i-used-oauth2-to-login-with-google
# https://developers.google.com/identity/gsi/web/guides/revoke
# https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
# https://stackoverflow.com/questions/67138365/disable-automatic-login-with-google-oauth-2-0
# https://petertc.medium.com/openid-connect-a27e0a3cc2ae
# https://developers.google.com/identity/sign-in/web/sign-in
# flask run -h localhost -p 5000, google sign in need localhost
@views.route('/google-sign-in', methods=['POST', 'OPTIONS'])
def google_sign_in():
    # request_data = json.loads(request.data)
    # token = request_data['id_token']
    response = jsonify({"test": "testdata"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Content-Type", 'application/json')
    response.headers.add("Access-Control-Allow-Headers", 'content-type')
    token = request.json['id_token']
    try:
        id_info = id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_OAUTH2_CLIENT_ID
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        userid = id_info['sub']
        email = id_info['email']
    except ValueError:
        # Invalid ValueError:
        raise ValueError('Invalid token.')
    print('登入成功')
    print(userid)
    print(email)
    user = User.query.filter_by(third_party_id=userid).first()
    if user:
        print("使用者存在")
        login_user(user, remember=True)
    else:
        new_user = User(email=email, password=None,
                        third_party="google", third_party_id=userid)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
    # flash('Account created!', category='success')
    # r = requests.post('http://localhost:5000/login', json={"email": None, "password": None, "third_party": "google", "third_party_id": userid})
    # print(r.status_code)
    # return r.status_code
    # return redirect(url_for('views.home'))
    print(response)
    return response


# @views.route('/google_sign_in', methods=['OPTIONS'])
# def google_sign_in():
#     response = jsonify({"test": "testdata"})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add("Access-Control-Allow-Headers", 'content-type')
#     return response
