from models.base_model import BaseModel
from models.user import User
from models.image import Image
import peewee as pw
from playhouse.hybrid import hybrid_property


class Donation(BaseModel):

    amount = pw.DecimalField(null=False)
    image = pw.ForeignKeyField(Image, backref="donations")
    user = pw.ForeignKeyField(User, backref="donations")
