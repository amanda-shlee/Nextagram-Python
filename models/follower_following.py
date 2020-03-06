import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property


class FollowerFollowing(BaseModel):
    idol = pw.ForeignKeyField(User, backref="fans")
    fan = pw.ForeignKeyField(User, backref="idols")
