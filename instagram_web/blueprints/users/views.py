from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, abort
from models.user import User
from models.image import Image
from models.follower_following import FollowerFollowing
from flask_login import login_required, login_user, current_user
from config import Config
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new_form', methods=['POST'])
def create():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    profile_image = request.form.get('profile_image')
    upload_image = request.form.get('upload_image')
    caption = request.form.get('caption')
    u = User(name=name, email=email, password=password,
             profile_image=profile_image, upload_image=upload_image, caption=caption)

    if u.save():
        flash("Your profile is created 🎉 ")
        return redirect(url_for('home'))
    else:
        for error in u.errors:
            flash(error)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.name == username)

    if not user:
        flash(f"No user with the username {username}")
        return redirect(url_for('users.index'))

    return render_template('users/show.html', user=user)


@users_blueprint.route('/', methods=["GET"])
def index():
    images = Image.select(Image, User).join(
        User).where(Image.user_id != current_user.id)

    return render_template("users/index.html", images=images)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    index = User.get_by_id(id)
    return render_template("users/edit.html", index=index)


@users_blueprint.route('/<id>/update', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)

    new_name = request.form.get('new_name')
    new_email = request.form.get('new_email')
    user.name = new_name
    user.email = new_email

    if user.save():
        flash("Successfully updated your profile")
        return redirect(url_for("users.edit", user=user, id=id))

    else:
        flash("Please try again")

        return render_template("users/edit.html")


@users_blueprint.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if "user_file" not in request.files:
        return flash("No user_file key in request.files")

    file = request.files["user_file"]

    if file.filename == "":
        return flash("Please select a file")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, Config.S3_BUCKET)
        user = User.update(profile_image=file.filename).where(
            User.id == current_user.id)
        user.execute()
        return redirect(url_for('sessions.profile', img=current_user.profile_image, name=current_user.name, id=current_user.id))

    else:
        return redirect(url_for('users.edit', id=current_user.id))
