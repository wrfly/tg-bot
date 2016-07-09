import requests
import json
# import subprocess
import threading

class bot():
	def __init__(self, ):
		self.TOKEN = '666'
		self.proxies = {
		  "http": "socks5://127.0.0.1:1080",
		  "https": "socks5://127.0.0.1:1080"
		}
		self.URL = 'https://api.telegram.org/bot'+self.TOKEN+'/'
		init_recieve = requests.post(self.URL+'getUpdates', proxies=self.proxies)
		init_json = json.loads(init_recieve.content)
		for r in init_json['result']:
			try:
				self.old_message_id = r['message']['message_id']
				self.offset = r['update_id']
				self.chat_id = r['message']['chat']['id']
			except Exception:
				pass

	def run(self):
		# print self.offset
		update = {
			"limit":10,
			"offset":self.offset-5
		}
		r = requests.get(self.URL+'getUpdates', proxies=self.proxies, data=update)
		j = json.loads(r.content)
		for r in j['result']:
			# try:
			# 	self.old_message_id = r['message']['message_id']
			# 	self.offset = r['update_id']
			# except Exception:
			# 	pass
			print r['message']['message_id']
			if r['message']['message_id'] > self.old_message_id:
				msg = r['message']['text']
				threading.Thread(target=self.send_msg(msg)).start()
		self.offset = r['update_id']
		self.old_message_id = r['message']['message_id']

	def send_msg(self, msg):
		send_data = {
			"chat_id":self.chat_id,
			"text": msg
			}
		requests.post(self.URL+'sendMessage', proxies=self.proxies, data=send_data)

b = bot()
while 1:
	b.run()
