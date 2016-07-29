import requests

def create_onereach_contact(contact_type, name="", number="", email=""):
	urls = {
		"career": "https://wapi.onereach.com/api/triggermessage/Sms/XgKOKRMS5aaaaN",
		"student": "https://wapi.onereach.com/api/triggermessage/Sms/Zev4RIMW5aaCa7",
		"parents": "https://wapi.onereach.com/api/triggermessage/Sms/O3JAKLMi5aaeaH",
		"enterprise": "https://wapi.onereach.com/api/triggermessage/Sms/MjJqKxM^5aa2at",
		"colleges": "https://wapi.onereach.com/api/triggermessage/Sms/P^J9KmMY5aakaO",
		"collegecareer": "https://wapi.onereach.com/api/triggermessage/Sms/NaJ!K8ME5aa8aA",
	}
	webhook_url = urls[contact_type]
	print "contact_type %s = url = %s" % (contact_type, webhook_url)
	apikey = "934b41b6-ad0b-4d48-b876-c5810aba557b"

	r = requests.post(webhook_url, 
		headers = {'apikey': apikey}, 
		json = {'To': number, "Email": email, "Name":name}
	)
	r.raise_for_status()
	print "Response %s" % r

