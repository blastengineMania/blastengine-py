from blastengine.MailBase import MailBase
from blastengine.Job import Job
from datetime import datetime, timedelta
from pathlib import Path
import requests
import json
import mimetypes
import tempfile
import csv
import time

class Bulk(MailBase):
	begin_url = 'https://app.engn.jp/api/v1/deliveries/bulk/begin'
	update_url = 'https://app.engn.jp/api/v1/deliveries/bulk/update'
	commit_url = 'https://app.engn.jp/api/v1/deliveries/bulk/commit'

	def to(self, email, insert_codes = {}):
		code = []
		for key in insert_codes:
			value = insert_codes[key]
			code.append({
				'key': f'__{key}__',
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
		if self.delivery_id is not None and len(self._to) > 0 and len(self._to) < 50:
			entity['to'] = self._to
		if 'name' in self._from:
			entity['from']['name'] = self._from['name']
		if self._html_part is not None:
			entity['html_part'] = self._html_part
		if self._unsubscribe is not None:
			entity['list_unsubscribe'] = {}
			if 'url' in self._unsubscribe:
				entity['list_unsubscribe']['url'] = self._unsubscribe['url']
			if 'email' in self._unsubscribe:
				entity['list_unsubscribe']['mailto'] = f'mailto:{self._unsubscribe["email"]}'
		return entity

	def csv_import(self, file_path, ignore_errors = False):
		job = Job(self.delivery_id, file_path, ignore_errors)
		job.import_file()
		return job
	
	def begin_csv(self):
		data = []
		for params in self._to:
			row = {}
			row['email'] = params['email']
			if params['insert_code'] is not None:
				for insert_code in params['insert_code']:
					row[insert_code['key']] = insert_code['value']
			data.append(row)
		with tempfile.NamedTemporaryFile('w', delete=False, newline='', suffix=".csv") as tmp_file:
			# CSVライターオブジェクトを作成
			writer = csv.DictWriter(tmp_file, fieldnames=data[0].keys(), quotechar = '"', quoting=csv.QUOTE_ALL)
			# ヘッダーを書き込む
			writer.writeheader()
			# dictオブジェクトを行として書き込む
			for row in data:
					writer.writerow(row)
		# close file
		tmp_file.close()
		job = self.csv_import(tmp_file.name)
		while job.finished() == False:
			time.sleep(5)

	def update(self):
		if len(self._to) > 50:
			return self.begin_csv()
		entity = self.generate_params()
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.put(f'{Bulk.update_url}/{self.delivery_id}', data=json.dumps(entity), headers=headers)
		res = self.handle_response(response)
		# Reset
		self._to = []
		return res

	def send(self, reservation_time = None):
		if reservation_time is None:
			return self.send_immediate()
		else:
			return self.send_schedule(reservation_time)
	
	def send_immediate(self):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.patch(f'{Bulk.commit_url}/{self.delivery_id}/immediate', headers=headers)
		return self.handle_response(response)
	
	def send_schedule(self, reservation_time):
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
