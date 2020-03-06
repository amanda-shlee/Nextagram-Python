from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.user import User
from models.follower_following import FollowerFollowing
from flask_login import LoginManager, login_user, login_required, current_user

follow_blueprint = Blueprint('follow', __name__, template_folder='templates')


# @follow_blueprint.route('/new', methods=['GET'])
# @login_required
# def new():
#     return render_template('users/show.html')


@follow_blueprint.route('/<idol_id>', methods=['POST'])
@login_required
def create(idol_id):

    idol = User.get_or_none(User.id == idol_id)

    if not idol:
        flash("User does not exist")
        return redirect(url_for('users.index'))

    f = FollowerFollowing(idol_id=idol.id, fan_id=current_user.id)

    if f.save():
        flash("Successfully followed your idol!")
        return redirect(request.referrer)

    else:
        flash("Go Away!")
        return redirect(url_for('users.index'))


@follow_blueprint.route('/<id>/delete')
@login_required
def delete(id):
    unfollow = FollowerFollowing.get_or_none(
        idol_id=id, fan_id=current_user.id)

    if unfollow.delete_instance():
        flash("Bye bye ")
        return redirect(request.referrer)

    else:
        flash("you will be a follower forever")
        return render_template("users/index.html")
