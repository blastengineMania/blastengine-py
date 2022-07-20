from blastengine.MailBase import MailBase
from datetime import datetime, timedelta
from pathlib import Path
import requests
import json
import mimetypes

class Bulk(MailBase):
	begin_url = 'https://app.engn.jp/api/v1/deliveries/bulk/begin'
	update_url = 'https://app.engn.jp/api/v1/deliveries/bulk/update'
	commit_url = 'https://app.engn.jp/api/v1/deliveries/bulk/commit'

	def to(self, email, insert_codes = []):
		code = []
		for insert_code in insert_codes:
			key = list(insert_code.keys())[0]
			value = list(insert_code.values())[0]
			code.append({
				'key': key,
				'value': value
			})
		self._to.append({
			'email': email,
			'insert_code': code
		})

	def begin(self):
		if len(self._attachments) > 0:
			return self.begin_attachments_mail()
		return self.begin_text_mail()

	def generate_params(self):
		entity = {
			'subject': self._subject,
			'text_part': self._text_part,
			'from': {
				'email': self._from['email']
			},
		}
		if self.delivery_id is None:
			entity['encode'] = self._encode
		if self.delivery_id is not None and len(self._to) > 0:
			entity['to'] = self._to
		if 'name' in self._from:
			entity['from']['name'] = self._from['name']
		if self._html_part is not None:
			entity['html_part'] = self._html_part
		return entity

	def update(self):
		entity = self.generate_params()
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.put(f'{Bulk.update_url}/{self.delivery_id}', data=json.dumps(entity), headers=headers)
		return self.handle_response(response)

	def send(self, reservation_time = None):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		if reservation_time is None:
			reservation_time = datetime.today() + timedelta(minutes=1)
		entity = {
			'reservation_time': reservation_time.astimezone().replace(microsecond=0).isoformat()
		}
		response = requests.patch(f'{Bulk.commit_url}/{self.delivery_id}', data=json.dumps(entity), headers=headers)
		return self.handle_response(response)
	
	def begin_text_mail(self):
		entity = self.generate_params()
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.post(Bulk.begin_url, data=json.dumps(entity), headers=headers)
		return self.handle_response(response)

	def begin_attachments_mail(self):
		entity = self.generate_params()
		headers = {
			'Authorization': f'Bearer {self.client.token}'
		}
		files = []
		for file_path in self._attachments:
			file = Path(file_path)
			files.append(('file', (file.name, open(file.resolve(), 'rb'), mimetypes.guess_type(file.resolve()))))
		files.append(('data', ('data.json', json.dumps(entity), 'application/json')))
		response = requests.post(Bulk.begin_url, files=files, headers=headers)
		return self.handle_response(response)
