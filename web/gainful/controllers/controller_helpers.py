from flask import Response


def ret_(message, status_code, type, data):
    import ujson
    response = Response()
    response.headers["Gain-Response"] = "Clem-Response"
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
