import re
from blastengine.MailBase import MailBase
from blastengine.Transaction import Transaction
from blastengine.Bulk import Bulk
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode

class Log(MailBase):

	def __init__(self):
		super().__init__()
		self.id = None
		self.last_response_code = None
		self.last_response_message = None

	@classmethod
	def find(cls, params = {}):
		headers = {
			'Authorization': f'Bearer {cls.client.token}',
			'content-type': 'application/json'
		}
		querystring = urlencode(params)
		response = requests.get(f'{cls.endpoint_url}/logs/mails/results?{querystring}', headers=headers)
		json_body = cls.handle_array_response(response)
		res = []
		for params in json_body:
			mail = Log()
			mail.sets(params)
			res.append(mail)
		return res
	
	def sets(self, params = {}):
		for key in params:
			self.set(key, params[key])
	
	def set(self, key, value):
		if value is None:
			return self
		if key == 'delivery_id':
			self.delivery_id = value
		elif key == "updated_time" or key == "created_time" or key == "delivery_time" or key == "open_time":
			setattr(self, key, datetime.fromisoformat(value))
		elif key == "email":
			self._to.append({
				'email': value
			})
		elif key == "delivery_type":
			self.delivery_type = value
		elif key == "status":
			self.status = value
		elif key == "maillog_id":
			self.id = value
		elif key == "last_response_code":
			self.last_response_code = value
		elif key == "last_response_message":
			self.last_response_message = value
		return self