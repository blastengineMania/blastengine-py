from blastengine.MailBase import MailBase
from pathlib import Path
import requests
import json
import mimetypes

class Transaction(MailBase):
	post_url = 'https://app.engn.jp/api/v1/deliveries/transaction'
	def send(self):
		if len(self._attachments) > 0:
			return self.send_attachments_mail()
		return self.send_text_mail()

	def generate_params(self):
		entity = {
			'subject': self._subject,
			'encode': self._encode,
			'text_part': self._text_part,
			'from': {
				'email': self._from['email']
			},
			'to': self._to
		}
		if 'name' in self._from:
			entity['from']['name'] = self._from['name']
		if len(self._insert_code) > 0:
			entity['insert_code'] = self._insert_code
		if self._html_part is not None:
			entity['html_part'] = self._html_part
		if self._unsubscribe is not None:
			entity['list_unsubscribe'] = {}
			if 'url' in self._unsubscribe:
				entity['list_unsubscribe']['url'] = self._unsubscribe['url']
			if 'email' in self._unsubscribe:
				entity['list_unsubscribe']['mailto'] = f'mailto:{self._unsubscribe["email"]}'
		return entity

	def send_text_mail(self):
		entity = self.generate_params()
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.post(Transaction.post_url, data=json.dumps(entity), headers=headers)
		return self.handle_response(response)

	def send_attachments_mail(self):
		entity = self.generate_params()
		headers = {
			'Authorization': f'Bearer {self.client.token}'
		}
		files = []
		fs = []
		for file_path in self._attachments:
			file = Path(file_path)
			f = open(file.resolve(), 'rb')
			files.append(('file', (file.name, f, mimetypes.guess_type(file.resolve()))))
			fs.append(f)
		files.append(('data', ('data.json', json.dumps(entity), 'application/json')))
		response = requests.post(Transaction.post_url, files=files, headers=headers)
		for f in fs:
			f.close()
		return self.handle_response(response)
