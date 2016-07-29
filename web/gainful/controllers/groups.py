from gainful.models import *
from gainful.onereach import *
from controller_helpers import *
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
import requests

groups = Blueprint('groups', __name__)

@groups.route("/")
@login_required
def list_groups():
    """Renders a list of all groups"""
    token = request.args.get('page_token', None)
    groups, next_page_token = Group.list(cursor=token)

    return ret_ok(data={ "groups" : groups})

@groups.route("/<path:group_id>")
@login_required
def get_group(group_id):
    """Returns group"""
    group = Group.query.get(group_id)

    if group:
        return ret_ok(data={ "name" : group.name, "members": group.members})
    else:
        return ret_error(message="Group doesn't exist")

@groups.route("/<path:group_id>/members")
@login_required
def list_members(group_id):
    """Renders a list of all groups"""
    token = request.args.get('page_token', None)
    group = Group.query.get(group_id)

    if group:
        return ret_ok(data={ "members" : group.members})
    else:
        return ret_error(message="Group doesn't exist")

@groups.route("/<path:group_id>/members/add", methods=["POST"])
@login_required
def add_members(group_id):
    """Renders a list of all groups"""
    member_ids = request.form.getlist('member_ids[]')
    print "member_ids %s" % member_ids
    group = Group.query.get(group_id)

    for member_id in member_ids:
        user = User.query.get(member_id)
        group.members.append(user)
    
    db.session.merge(group)
    db.session.commit()

    if group:
        return ret_ok(data={ "members" : group.members})
    else:
        return ret_error(message="Group doesn't exist")
