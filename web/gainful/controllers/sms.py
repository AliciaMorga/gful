from flask import Blueprint, request
from gainful.helpers import *
import twilio.twiml

sms = Blueprint('sms', __name__)

@sms.route('/reply', methods=['GET', 'POST'])
def reply():
    """Reply to an inbound sms"""
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return str(resp)
