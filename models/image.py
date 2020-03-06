from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    upload_image = pw.CharField(null=True)
    caption = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def has_upload_image(self):
        return f"https://nextagram-amanda.s3.amazonaws.com/{self.upload_image}"

    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount
        return round(total)
