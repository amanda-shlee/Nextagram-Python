from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, abort
from models.user import User
from models.image import Image
from flask_login import login_required, login_user, current_user
from config import Config
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/new', methods=["POST"])
@login_required
def upload_img():

    if "user_file" not in request.files:
        return flash("No user_file key in request.files")

    file = request.files["user_file"]
    caption = request.form.get('caption')

    if file.filename == "":
        return flash("Please select a file")

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, Config.S3_BUCKET)

        p = Image(
            user=current_user.id, upload_image=file.filename, caption=caption)
        p.save()

        return redirect(url_for("sessions.profile", id=current_user.id))

    else:
        flash("Please try again 🥺")
        return render_template("sessions/profile.html")
