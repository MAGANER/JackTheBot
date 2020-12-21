import requests
import random
from bs4 import BeautifulSoup


class ImageGetter:
	def __init__(self, url):
		self.data = {}
		self.data["link"] = url
	
	def get_html_page(self, headers=None, params=None):
		return requests.get(self.data["link"],headers=headers,params=params)
	
	def parse_html_page(self,page):
		return BeautifulSoup(page.text,"html.parser")
	