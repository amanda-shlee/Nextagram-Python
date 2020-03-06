from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from models.user import User
from models.base_model import BaseModel
from instagram_web.util.google_oauth import oauth
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint(
    'sessions', __name__, template_folder='templates')


@sessions_blueprint.route('/login', methods=["GET"])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/new_form', methods=["POST"])
def login():
    password_to_check = request.form['password']
    user = User.get_or_none(User.email == request.form.get('email'))

    if user:
        hashed_password = user.password
        result = check_password_hash(hashed_password, password_to_check)
        # flash("You're almost there")
        if result:
            login_user(user)
            flash("Successfully login 😉")
            return redirect(url_for('sessions.profile', id=current_user.id))

        else:
            flash("Please check your password again 😔")
            return render_template('sessions/new.html')

    else:
        flash("Have you signed up? 🤨")
        return render_template('sessions/new.html')


@sessions_blueprint.route('/google_login')
def google_login():
    redirect_uri = url_for('sessions.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route('/authorize/google')
def authorize():

    oauth.google.authorize_access_token()
    email = oauth.google.get(
        "https://www.googleapis.com/oauth2/v2/userinfo").json()['email']
    user = User.get_or_none(User.email == email)

    if user:
        login_user(user)
        return redirect(url_for('sessions.profile', id=current_user.id))
    else:
        flash("go away")
        return(redirect(url_for('sessions.login')))


@sessions_blueprint.route('/profile/<id>', methods=["GET"])
@login_required
def profile(id):
    user = User.get_by_id(id)
    return render_template("sessions/profile.html",  user=user)


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    flash("Bye bye 🥺")
    return redirect(url_for("sessions.new"))
