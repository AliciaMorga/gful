from gainful.models import *
from gainful.onereach import *
from controller_helpers import *
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
import requests

users = Blueprint('users', __name__)

@users.route("/")
@login_required
def list():
    """Renders a list of all users"""
    token = request.args.get('page_token', None)
    users, next_page_token = User.list(cursor=token)
    return ret_ok(data={"users" : users})

@users.route('/<id>')
@login_required
def view(id):
    """View a specific user

    Args:
        id (int): User id
    """
    user = User.read(id)
    return render_template("view.html", user=user)

# [START add]
@users.route('/add', methods=['GET', 'POST'])
def add():
    """Creates a user"""
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        # contact_type should be a hidden post field. defaults to student for backwards compatibility
        contact_type = data.get('contact_type', 'student')
        name = data.get('name')
        mobile_number = data.get('mobile_number')
        email = data.get('email')

        # Unbounce webhook
        json = data.get('data.json')
        if json:
            json_dict = json.loads(json)
            name = json_dict.get('name')[0] if json_dict.get('name') else name
            mobile_number = json_dict.get('mobile_number')[0] if json_dict.get('mobile_number') else mobile_number
            email = json_dict.get('email')[0] if json_dict.get('email') else email

        user = User.create({'name': name, 'mobile_number': mobile_number, 'email': email})

        print "Creating contact number %s" % mobile_number
        create_onereach_contact(contact_type=contact_type, name=name, number=mobile_number, email=email)
        return redirect("https://www.getgainful.com/thank-you")
        # return redirect(url_for('.view', id=user['id']))

    return render_template("form.html", action="Add", user={})
# [END add]

@users.route('/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Edit a user"""
    user = User.read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        user = User.update(data, id)

        return redirect(url_for('.view', id=user['id']))

    return render_template("form.html", action="Edit", user=user)

@users.route('/<id>/delete')
@login_required
def delete(id):
    """ Delete a user"""
    User.delete(id)
    return redirect(url_for('.list'))
