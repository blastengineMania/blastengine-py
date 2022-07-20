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
			'to': ",".join(self._to)
		}
		if 'name' in self._from:
			entity['from']['name'] = self._from['name']
		if self._html_part is not None:
			entity['html_part'] = self._html_part
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
		for file_path in self._attachments:
			file = Path(file_path)
			files.append(('file', (file.name, open(file.resolve(), 'rb'), mimetypes.guess_type(file.resolve()))))
		files.append(('data', ('data.json', json.dumps(entity), 'application/json')))
		response = requests.post(Transaction.post_url, files=files, headers=headers)
		return self.handle_response(response)
