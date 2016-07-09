import requests
import json
import subprocess

TOKEN = 'YOURTOKEN'

proxies = {
  "http": "socks5://127.0.0.1:1080",
  "https": "socks5://127.0.0.1:1080"
}

URL = 'https://api.telegram.org/bot'+TOKEN+'/'

METHOD_NAME = 'getUpdates'

r = requests.post( URL+METHOD_NAME, proxies=proxies)
j = json.loads(r.content)
offset = int(j['result'][0]['update_id'])

old_message_id = 0

while 1:
	METHOD_NAME = 'getUpdates'
	update = {
		"limit":5,
		"offset":offset
	}
	r = requests.get(URL+METHOD_NAME, proxies=proxies, data=update)
	j = json.loads(r.content)

	chat_id = j['result'][-1]['message']['chat']['id']

	message_id = j['result'][-1]['message']['message_id']

	got_text = j['result'][-1]['message']['text']
	
	try:
		return_text = subprocess.check_output(got_text.split(' '))
	except Exception:
		return_text = got_text

	if old_message_id != message_id:
		offset += 1
		METHOD_NAME = 'sendMessage'
		old_message_id = message_id
		send_data = {
			"chat_id":chat_id,
			"text": return_text
			}
		requests.post(URL+METHOD_NAME, proxies=proxies, data=send_data)
