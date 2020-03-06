from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property, hybrid_method


class User(BaseModel):
    name = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.TextField(unique=True)
    profile_image = pw.CharField(null=True)

    def validate(self):
        existing_username = User.get_or_none(
            User.name == self.name)

        # if the username exists and this username's id is NOT in self.id
        if existing_username and not existing_username.id:
            self.errors.append("Username has been taken!")

        existing_email = User.get_or_none(User.email == self.email)

        if existing_email and not existing_email.id:
            self.errors.append("Error, please fixed!")

        if not self.id and len(self.password) < 6:
            self.errors.append(
                'Password has to be longer than 6 characters.')

        # if not self.id and re.search(r"\d", self.password):
        #     self.errors.append(
        #         "Password must contain at least one digit")

        if not self and any(char.isupper()for char in self.password):
            self.errors.append(
                'Password requires at least an Upper Case Letter.')

        if not self and any(char.islower()for char in self.password):
            self.errors.append(
                'Password requires at least an Lower Case Letter'
            )

        else:
            self.password = generate_password_hash(self.password)

        if User.get_or_none(User.email == self.email):
            self.errors.append('Email is not unique')

    @hybrid_property
    def has_profile_image(self):
        return f"https://nextagram-amanda.s3.amazonaws.com/{self.profile_image}"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_anonymous(self):
        return False

    @hybrid_method
    def is_following(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == user.id) & (FollowerFollowing.fan_id == self.id)) else False

    @hybrid_method
    def is_followed_by(self, user):
        from models.follower_following import FollowerFollowing
        return True if FollowerFollowing.get_or_none((FollowerFollowing.idol_id == self.id) & (FollowerFollowing.fan_id == user.id)) else False
