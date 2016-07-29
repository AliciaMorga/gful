from wit import Wit

app_id = "570dd7ea-32ca-4483-aba5-344d3173ef8a"
wit_token = "5ZONHELFNJ2DKET2M3HAPGJTUCD7GZEM"

def wit_client():
	client = Wit(wit_token, get_actions())
	return client

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
	# Sanitize or normalize data before storing it in the context
	print "merge %s %s %s" % (context, entities, msg)
	location = first_entity_value(entities, 'location')
	if location:
		context['location'] = location
	return context

def error(session_id, context, e):
    print(str(e))

def show_map(session_id, context):
    print("map called %s" % str(context))
    return context

def get_actions():
	return {
		'say': say,
		'merge': merge,
		'error': error,
		'map': show_map,
	}
