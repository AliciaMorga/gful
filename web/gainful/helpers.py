from flask import Response, json, request, current_app, abort, redirect, url_for, g, session
import error_codes

############
# Requests
############
def jsonify(data):
	return json.loads(unicode(data, "ISO-8859-1"))

############
# responses
############
def ret_(message, status_code, type, data):
	import ujson
	response = Response()
	response.headers["Gainful-Response"] = "Gainful-Response"
	response.mimetype = "application/json"
	response.status_code = status_code
	response.data = ujson.dumps(
		{ "type" : type, "message" : message, "data" : data }
	)
	return response

def ret_ok(message=None, status_code=200, data=None):
	return ret_(message, status_code, "ok", data)

def ret_error(message=None, status_code=400):
	return ret_(message, status_code, "error", None)

def ret_bad_request(message=error_codes.INVALID_PARAMETERS):
	return ret_error(message, 400)

def ret_forbidden(message=None):
	return ret_error(message, 403)

def ret_not_found(message=None):
	return ret_error(message, 404)

def ret_unauthorized(message=None):
	return ret_error(message, 401)

def ret_server_error(message=None):
	return ret_error(message, 500)

def ret_not_implemented():
	return ret_error("", 501)

