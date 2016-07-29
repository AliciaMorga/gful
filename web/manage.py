from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import config
import requests
import json

from gainful.onereach import *
from gainful.witai import *
from gainful.search import search_answers
from gainful.controllers import auth

app = Flask(__name__)
# configure your app
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def onereach_signup():
	# curl -H "Content-Type: application/json" --header "apikey: 934b41b6-ad0b-4d48-b876-c5810aba557b" -X POST -d '{"To":"9494362573"}' https://wapi.onereach.com/api/triggermessage/Sms/7OJbQwM05aaMaE
	print "creating onereach contact"
	create_onereach_contact(contact_type="student", name="Samir Naik", number="9494362573", email="samir.naik@gmail.com")

@manager.command
def wit_message():
	client = wit_client()
	session_id = 'my-user-session-42'
	context0 = {}
	context1 = client.run_actions(session_id, 'where is the bookstore?', context0)
	print('The session state is now: ' + str(context1))
	context2 = client.run_actions(session_id, 'San Francisco', context1)
	print('The session state is now: ' + str(context2))
	# resp = client.message('where is the bookstore')
	# print('Yay, got Wit.ai response: ' + str(resp))

@manager.command
def search(term):
	return search_answers(term)

@manager.command
def create_admin_user(email, number, password):
	return auth.create_confirmed_user(email, number, password)

if __name__ == "__main__":
	manager.run()

