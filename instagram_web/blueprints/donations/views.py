import os
import requests
from flask_login import login_required, current_user
from instagram_web.util.braintree import gateway
from instagram_web.util.mailhelper import send_simple_message
from models.image import Image
from models.user import User
from models.donation import Donation
from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash

donations_blueprint = Blueprint(
    'donations', __name__, template_folder="templates")


@donations_blueprint.route('<image_id>/new', methods=['GET'])
@login_required
def new(image_id):
    image = Image.get_or_none(Image.id == image_id)
    client_token = gateway.client_token.generate()

    if client_token:
        return render_template('donations/new.html', image=image, client_token=client_token)


@donations_blueprint.route('/<image_id>', methods=['POST'])
@login_required
def donation(image_id):
    image = Image.get_or_none(Image.id == image_id)
    nonce = request.form.get("payment_method_nonce")
    amount = request.form.get("amount")

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    donate = Donation(amount=amount, image_id=image.id,
                      user_id=current_user.id)

    if result:
        donate.save()
        # send_simple_message()
        flash("Donations completed")
        return redirect(url_for('donations.new', image_id=image.id, nonce=nonce, amount=amount))
