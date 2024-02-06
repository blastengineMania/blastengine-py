import json
from datetime import datetime, timezone, timedelta
import requests

class MailBase:
	clinet = None
	base_url = 'https://app.engn.jp/api/v1/deliveries'
	endpoint_url = 'https://app.engn.jp/api/v1'

	def __init__(self):
		self.delivery_id = None
		self._subject = ''
		self._to = []
		self._cc = []
		self._bcc = []
		self._from = {}
		self._encode = 'UTF-8'
		self._insert_code = None
		self._text_part = ''
		self._html_part = None
		self._unsubscribe = None
		self._attachments = []
		self.delivery_type = None
		self.status = None
		self.total_count = None
		self.sent_count = None
		self.drop_count = None
		self.hard_error_count = None
		self.soft_error_count = None
		self.open_count = None
		self.delivery_time = None
		self.reservation_time = None
		self.created_time = None
		self.updated_time = None		
		self.job_id = None

	def sets(self, params):
		for key in params:
			self.set(key, params[key])
		return self
	def set(self, key, value):
		if value is None:
			return self
		if key == "updated_time" or key == "created_time" or key == "reservation_time" or key == "delivery_time":
			setattr(self, key, datetime.fromisoformat(value))
		elif key == "delivery_id":
			self.delivery_id = value
		elif key == "subject":
			self._subject = value
		elif key == "delivery_type":
			self.delivery_type = value
		elif key == "status":
			self.status = value
		elif key == "from":
			self._from = {
				'email': value['email'],
				'name': value['name']
			}
		return self

	def subject(self, value = None):
		if value is None:
			return self._subject
		self._subject = value
	
	def to(self, email):
		self._to = email
	
	def cc(self, email):
		self._cc.append(email)
	
	def bcc(self, email):
		self._bcc.append(email)
	
	def from_address(self, email = None, name = ''):
		if email is None:
			return self._from
		self._from = {
			'email': email,
			'name': name
		}
	
	def insert_code(self, key, value):
		if self._insert_code == None:
			self._insert_code = []
		self._insert_code.append({
			'key': key,
			'value': value
		})
	
	def encode(self, value):
		self._encode = value
	
	def text_part(self, value):
		self._text_part = value

	def html_part(self, value):
		self._html_part = value
	
	def unsubscribe(self, *, url=None, email=None):
		if url is not None or email is not None:
			self._unsubscribe = {}
		if url is not None:
			self._unsubscribe["url"] = url
		if email is not None:
			self._unsubscribe["email"] = email

	def attachments(self, file_path):
		self._attachments.append(file_path)

	@classmethod
	def handle_error(self, response):
		json_body = json.loads(response.content)
		if response.status_code > 300:
			messages = []
			for key in json_body['error_messages']:
				messages.append(f"{key}: {', '.join(json_body['error_messages'][key])}")
			raise Exception("\n".join(messages))
		return json_body
	
	@classmethod
	def handle_array_response(self, response):
		json_body = MailBase.handle_error(response)
		return json_body['data']
	
	def handle_job_response(self, response):
		json_body = MailBase.handle_error(response)
		self.job_id = json_body['job_id']
		return self.job_id

	def handle_response(self, response):
		json_body = MailBase.handle_error(response)
		self.delivery_id = json_body['delivery_id']
		return self.delivery_id
	
	def delete(self):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.delete(f'{MailBase.base_url}/{self.delivery_id}', headers=headers)
		return self.handle_response(response)

	def get(self):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.get(f'{MailBase.base_url}/{self.delivery_id}', headers=headers)
		self.handle_response(response)
		json_body = json.loads(response.content)
		self.delivery_id = json_body['delivery_id']
		self.fromAddress(json_body['from']['email'], json_body['from']['name'])
		self.delivery_type = json_body['delivery_type']
		self.status = json_body['status']
		self.subject(json_body['subject'])
		self.text_part(json_body['text_part'])
		self.html_part(json_body['html_part'])
		self.total_count = json_body['total_count']
		self.sent_count = json_body['sent_count']
		self.drop_count = json_body['drop_count']
		self.hard_error_count = json_body['hard_error_count']
		self.soft_error_count = json_body['soft_error_count']
		self.open_count = json_body['open_count']
		self.delivery_time = json_body['delivery_time']
		self.reservation_time = json_body['reservation_time']
		self.created_time = json_body['created_time']
		self.updated_time = json_body['updated_time']


