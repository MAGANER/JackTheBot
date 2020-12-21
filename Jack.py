from ImageGetter import *
from Base import Talker
import random
import datetime


HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                         "Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36",
           "accept": "*/*"}
		   
class Jack(Talker):
	def __init__(self):
		super().__init__("Джек")
		self.buy_words = ("вали","давай","до свидания","cyal8","пока","прощай")
		self.greetings = ("привет","здорово","hii")
		
		self.joke_actions = ("пошёл","сел","умер","родился","упал","посмеялся")
		self.finish = ("и застрелился","им оказался ты","протрезвел")
		self.joke_object = ""
		
		self.meme_master = ImageGetter("http://risovach.ru/all")
		
		#joke variables
		self.wanna_joke = False
		self.tell_joke  = False
		###
				
		self.actions = {
					"привет" : self.say_hello,
					"пока" : self.say_buy,
					"расскажи анекдот": self.tell_a_joke,
					"выбери": self.choose,
					"кидай мем":self.get_meme,
				}
	def is_command(self, text):
		for command in self.actions.keys():
			if command in text:
				return command
		return ""
	
	def get_images(self,html):
		# data can be contained with link/a tag
		data1 = html.find_all("img")

		
		#combine them and convert to strings
		data = data1
		data = list(map(lambda n: str(n),data))
		paths= list(filter(lambda string: "src" in string, data))
		
		def get_href_data(href):
			href_pos = href.find('src="')
			
			find_value_len = 5
			_href = href[href_pos+find_value_len:]
			
			end_pos = _href.find('"')
			return _href[:end_pos]
		href_data = list(map(get_href_data,paths))	
		
		is_png    = lambda data:".png" or ".jpg" or ".jpeg" in data
		image_data =list(filter(is_png,href_data))
		 
		return image_data
		
	def say_hello(self):
		self.send_message(self.last_chat_id,random.choice(self.greetings))
	def say_buy(self):
		self.send_message(self.last_chat_id,random.choice(self.buy_words))
		
	def get_meme(self):
		number = str(random.randint(1,100))
		self.meme_master.data["link"]=self.meme_master.data["link"] +"/"+number
		html = self.meme_master.get_html_page(headers=HEADERS)
		page = self.meme_master.parse_html_page(html)

		images = self.get_images(page)	
		
		if(len(images)>1):
			images = list(filter(lambda n: "share" not in n,images))
			images = list(filter(lambda n: "icons" not in n,images))
			
			image = "http://risovach.ru/"+random.choice(images)
			
			self.send_message(self.last_chat_id,"коромче всемго ям нагёл "+str(len(images)))
			self.send_image(self.last_chat_id,image)
		else:
			self.send_message(self.last_chat_id,"нехуй кидать из "+number)
		
		self.meme_master.data["link"] = "http://risovach.ru/all"
	
	#joke processing
	def tell_a_joke(self):
		self.send_message(self.last_chat_id,"о ком?")
		self.wanna_joke = True
	def process_joke(self):
			if self.tell_joke:
				self.joke_object = self.last_chat_text
				joke = self.joke_object+" "+random.choice(self.joke_actions)+" "+random.choice(self.finish)
				self.send_message(self.last_chat_id,joke)
				self.tell_joke = False
				self.wanna_joke= False
			if self.wanna_joke:
				self.tell_joke = True	
	###
	
	def choose(self):
		variants = self.last_chat_text.split(" ")
		if len(variants) > 1:
			variants = list(filter(lambda x:x != "или" and x != "выбери",variants))
			answer = "лучше "+random.choice(variants)
			self.send_message(self.last_chat_id,answer)
		else:
			self.send_message(self.last_chat_id,"а выбирать то нечего")
	
	#monkey regime
	def say_bullshit(self):
		number = random.random()
		if number > 0.5:
			words = self.last_chat_text.split(" ")
			word  = random.choice(words)
			
			answer = ("серьёзно?","лол","я так не думаю...","лучше бы пил..")
			to_send = random.choice(answer)+" "+word
			self.send_message(self.last_chat_id,to_send)
	###
	def say_every_hour_bullshit(self):
		bullshit = ("убей себя об стену","хуан-пидосян сгнившая на западе папироса","ааааааааа!","хо-хо.. иди на хуй","я съел мандарин(манду)")
		time = datetime.datetime.now()
		if time.minute == 0 and time.second == 0 and time.microsecond == 0:
			self.send_message(self.last_chat_id,random.choice(bullshit))
			
	def reflect(self):
		if "соси" in self.last_chat_text:
			pass
		
	def run(self):
		do_anything = self.last_message_id != self.curr_message_id 
		if do_anything:
			command = self.is_command(self.last_chat_text)
			if command in self.actions.keys():
				self.actions[command]()
			elif not self.wanna_joke:
				self.send_message(self.last_chat_id,"не понял "+command)
			self.last_message_id = self.curr_message_id
			
			self.say_bullshit()
			self.process_joke()
		
		self.say_every_hour_bullshit()

bot = Jack()			
def main(bot):
	while True:
		bot.update_me()
		bot.run()
if __name__ == '__main__':  
	try:
		main(bot)
	except KeyboardInterrupt:
		bot.send_message(bot.last_chat_id,"leaving this world..")
		exit()
	
	
	
	