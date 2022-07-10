import json
import urllib.parse
import os
import sys
import hashlib
import base64
from blastengine.MailBase import MailBase

class Blastengine:
	def __init__(self, user_id, api_key):
		self.user_id = user_id
		self.api_key = api_key
		self.token = self.generate_token()
		MailBase.client = self
	
	def generate_token(self):
		digest = hashlib.sha256(f'{self.user_id}{self.api_key}'.encode()).hexdigest()
		return base64.b64encode(digest.encode()).decode('utf-8')
