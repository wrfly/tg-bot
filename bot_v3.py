import requests
import json
import subprocess
import threading

class bot():
	def __init__(self, ):
		self.TOKEN = 'YOURTOKEN'
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
		update = {
			"limit":10,
			"offset":self.offset-5
		}
		r = requests.get(self.URL+'getUpdates', proxies=self.proxies,\
			data=update)
		j = json.loads(r.content)
		for r in j['result']:
			self.handle_msg(r)
		self.offset = r['update_id']

	def send_msg(self, data, data_type):
		def sendMessage(msg = data):
			send_data = {
				"chat_id":self.chat_id,
				"text": msg
				}
			requests.post(self.URL+'sendMessage', proxies=self.proxies,\
				data=send_data)
		def sendPhoto(photoID = data):
			send_data = {
				"chat_id":self.chat_id,
				"photo": photoID
				}
			requests.post(self.URL+'sendPhoto', proxies=self.proxies,\
				data=send_data)
		def sendSticker(stickerId = data):
			send_data = {
				"chat_id":self.chat_id,
				"sticker": stickerId
				}
			requests.post(self.URL+'sendSticker', proxies=self.proxies,\
				data=send_data)
		def sendVoice(voiceID = data):
			send_data = {
				"chat_id":self.chat_id,
				"voice": voiceID
				}
			requests.post(self.URL+'sendVoice', proxies=self.proxies,\
				data=send_data)

		if data_type == 'msg':
			t = sendMessage()
		elif data_type == 'photo':
			t = sendPhoto()
		elif data_type == 'sticker':
			t = sendSticker()
		elif data_type == 'voice':
			t = sendVoice()
		threading.Thread(target=t).start()
		# threading.Thread(target=sendMessage()).start()

	def handle_msg(self, data):
		if 'message' in data:
			m = data['message']
		elif 'edited_message' in data:
			m = data['edited_message']

		if 'text' in m:
			msg_type = 'msg'
			msg = m['text']
			try:
				# excute command (if msg is a command)
				msg = subprocess.check_output(m['text'].split(' '))
			except Exception:
				msg = str(m['message_id'])+':'+m['text']
		elif 'voice' in m:
			msg_type = 'voice'
			msg = m['voice']['file_id']
		elif 'sticker' in m:
			msg_type = 'sticker'
			msg = m['sticker']['file_id']
		elif 'photo' in m:
			msg_type = 'photo'
			msg = m['photo'][-1]['file_id']
		else:
			msg_type = 'msg'
			msg = 'Nanana'

		if m['message_id'] > self.old_message_id:
			# send message
			self.send_msg(msg, msg_type)
			# update message id
			self.old_message_id = m['message_id']
		

b = bot()
while 1:
	b.run()