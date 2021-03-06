from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# import requests

from app import db
from app.model.models import User


from google.oauth2 import id_token
import google.auth.transport.requests as google_requests

from app.settings import GOOGLE_OAUTH2_CLIENT_ID

'''
auth 負責 有關權限的 url 對應處理，
'''
# Make auth' Blueprint instance
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user, google_oauth2_client_id=GOOGLE_OAUTH2_CLIENT_ID)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        # first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = sign_up_user_exist(email)
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 character.', category='error')
        # elif len(first_name) < 2:
            # flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            print(email)
            new_user = User(email=email, password=generate_password_hash(
                password1, method='sha256'), third_party=None, third_party_id=None)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            # flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user, google_oauth2_client_id=GOOGLE_OAUTH2_CLIENT_ID)


def sign_up_user_exist(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return "User is already exist"
    return
    