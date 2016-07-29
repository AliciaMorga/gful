from gainful.models import *
from gainful.onereach import *
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
import requests
from datetime import datetime

customer_admin = Blueprint('customer_admin', __name__)

@customer_admin.route("/")
@login_required
def home():
    """Renders customer admin home page"""
    return render_template("customer_admin.html")

@customer_admin.route("/scheduler", methods=['GET', 'POST'])
@login_required
def scheduler():
    """Renders message scheduler page"""
    if request.method == "POST":
        handle_scheduled_message()
        flash('Your message is scheduled!')

    groups, next_page_token = Group.list()
    dt = datetime.now()

    cal_default = dt.strftime('%Y-%m-%d')
    time_default = dt.strftime('%H:%M')
    print "cal_default %s" % cal_default
    return render_template("scheduler.html", 
        groups=groups, 
        cal_default=cal_default, 
        time_default=time_default)

@customer_admin.route("/students", methods=['GET', 'POST'])
@login_required
def students():
    """Renders students page"""
    if request.method == "POST":
        # TODO(snaik): validate inputs
        data = request.form.to_dict(flat=True)
        print "create user", data
        User.create(data)

        contact_type = 'student'
        name = data.get('name')
        mobile_number = data.get('mobile_number')
        email = data.get('email')

        # TODO(snaik): need a way to create a onereach contact without sending a text
        print "Creating onereach contact %s, %s" % (name, mobile_number)
        create_onereach_contact(contact_type=contact_type, name=name, number=mobile_number, email=email)

    token = request.args.get('page_token', None)
    users, next_page_token = User.list(cursor=token)

    return render_template(
        "students.html",
        users=users,
        next_page_token=next_page_token)

@customer_admin.route("/groups", methods=['GET', 'POST'])
@login_required
def groups():
    if request.method == 'POST':
        # TODO(snaik): validate inputs
        """Creates a group"""
        data = request.form.to_dict(flat=True)
        print "create group", data
        Group.create(data)

    # Render group page
    token = request.args.get('page_token', None)
    groups, next_page_token = Group.list(cursor=token)
    group = Group.query.get(1)

    return render_template(
        "groups.html",
        groups=groups,
        users=group.members,
        next_page_token=next_page_token)

@customer_admin.route("/reports")
@login_required
def reports():
    """Renders reports home page"""
    return render_template("reports.html")

def handle_scheduled_message():  
    data = request.form.to_dict(flat=True)
    message = data.get('message')
    group_id = data.get('group')

    group = Group.query.get(group_id)
    print "Send message\n=============\ngroup: %s\nmembers: %s\ncontent: %s\n" % (group.name, group.members, message)
