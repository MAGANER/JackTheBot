import requests

#main class for every bot
class Bot:
	def __init__(self):
		self.url = "https://api.telegram.org/bot1425943282:AAGkW227xILwjvGTvLeiPQSCaV5EBILxkts/"
		
	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		resp = requests.get(self.url + method, params)
		result_json = resp.json()['result']
		return result_json
	
	def get_last_update(self):
		get_result = self.get_updates()

		if len(get_result) > 0:
			last_update = get_result[-1]
		else:
			last_update = get_result[len(get_result)]

		return last_update
	
	def send_message(self, chat_id, text):
		params = {'chat_id': chat_id, 'text': text}
		method = 'sendMessage'
		resp = requests.post(self.url + method, params)
		return resp
		
	def send_image(self, chat_id, url):
		params = {"chat_id":chat_id,"photo": url}
		method = "SendPhoto"
		resp = requests.post(self.url+method,params)
		return resp

#main class for chat-bot
class Talker(Bot):
	def __init__(self, name):
		Bot.__init__(self)
		self.last_update = 0
		
		self.last_update_id = -1
		self.last_message_id= -1
		self.last_chat_text = ""
		self.last_message   = ""
		self.last_chat_id   = -1
		self.last_chat_name = ""
		self.curr_message_id= -1
		
		self.name = name
		
	def is_talking_to_myself(self,text):
		return "/"+name in text
	def get_command(self,text):
		return text[len(self.name):]
	
	
	def update_me(self):
		Bot.get_updates(self)
		self.last_update = Bot.get_last_update(self)
		
		self.last_update_id = self.last_update['update_id']
		if "message" in self.last_update.keys():
			if "text" in self.last_update["message"]:
				self.last_chat_text = self.last_update['message']['text']
			self.last_chat_id   = self.last_update['message']['chat']['id']
			self.last_chat_name = self.last_update['message']['from']['first_name']
			self.curr_message_id= self.last_update['message']['message_id']
			
		if "text" in self.last_update["message"]:
			self.last_message = self.last_update["message"]["text"]
