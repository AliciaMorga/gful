# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from werkzeug.security import generate_password_hash, \
     check_password_hash

builtin_list = list

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    _init_admin(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

class BaseModel(object):
    # serialization helper
    def to_dict(self, **kwargs):
        result = {}

        cls = type(self)
        try:
            cols = cls._clem_cols
        except:
            cols = cls.__mapper__.c.items()
            cls._clem_cols = cols

        for key, val in cols:
            if key == "password":
                continue
            if not key in self.__dict__:
                continue
            o = self.__dict__[key]
            if o == None and val.nullable:
                continue
            if type(o) == datetime:
                o = o.isoformat()
            result[key] = o

        # serialize extra information from arguments
        result.update(kwargs)

        return result

    # [START list]
    @classmethod
    def list(cls, limit=10, cursor=None):
        cursor = int(cursor) if cursor else 0
        query = (cls.query
                 .order_by(cls.name)
                 .limit(limit)
                 .offset(cursor))
        instances = builtin_list(map(from_sql, query.all()))
        next_page = cursor + limit if len(instances) == limit else None
        return (instances, next_page)
    # [END list]


    # [START read]
    @classmethod
    def read(cls, id):
        result = cls.query.get(id)
        if not result:
            return None
        return from_sql(result)
    # [END read]

    # [START create]
    @classmethod
    def create(cls, data):
        instance = cls(**data)
        db.session.add(instance)
        db.session.commit()
        return from_sql(instance)
    # [END create]

    # [START update]
    @classmethod
    def update(cls, data, id):
        user = cls.query.get(id)
        for k, v in data.items():
            setattr(user, k, v)
        db.session.commit()
        return from_sql(user)
    # [END update]

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()



# [START model]
class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    mobile_number = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=True)
    date_confirmed = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<User(name='%s', mobile_number=%s, email=%s)" % (self.name, self.mobile_number, self.email)

    def __init__(self, email=None, mobile_number=None, password=None, name=None):
        self.email = email
        self.mobile_number = mobile_number
        self.name = name
        if password:
            self.set_password(password)

    @classmethod
    def get_by_email(cls, email):
        return (User.query
            .filter(User.email == email)
            .one())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# [END model]

group_members = db.Table('group_members',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

# [START model]
class Group(db.Model, BaseModel):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    members = db.relationship('User', secondary=group_members)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Group(name='%s')" % (self.name)
# [END model]

# [START model]
class Org(db.Model, BaseModel):
    __tablename__ = 'orgs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Org(name='%s')" % (self.name)
# [END model]

# [START model]
class Answer(db.Model, BaseModel):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('orgs.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    org = db.relationship("Org", backref="answers")
    question = db.Column(db.String(255))
    answer = db.Column(db.String(1023))

    def __repr__(self):
        return "<Answer(question='%s', answer='%s')" % (self.question, self.answer)

# [END model]

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")

class VisiblePkView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

class AnswerModelView(VisiblePkView):
    column_searchable_list = ('question', 'answer')

def _init_admin(app):
    """
    Initialize the admin and add views
    """
    admin = Admin(app, name='gainful', template_mode='bootstrap3')

    admin.add_view(VisiblePkView(User, db.session))
    admin.add_view(VisiblePkView(Org, db.session))
    admin.add_view(AnswerModelView(Answer, db.session))
    admin.add_view(VisiblePkView(Group, db.session))

if __name__ == '__main__':
    _create_database()
