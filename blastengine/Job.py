from blastengine.MailBase import MailBase
from pathlib import Path
import json
import requests

class Job(MailBase):
	def __init__(self, delivery_id, file_path, ignore_errors):
		self.delivery_id = delivery_id
		self.file_path = file_path
		self.ignore_errors = ignore_errors
		self.import_url = f'https://app.engn.jp/api/v1/deliveries/{self.delivery_id}/emails/import'
		self.percentage = None
		self.status = None
		self.success_count = None
		self.total_count = None
		self.failed_count = None
		self.error_file_url = None
	
	def import_file(self):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
		}
		entity = {
			'ignore_errors': self.ignore_errors
		}
		files = []
		file = Path(self.file_path)
		f = open(file.resolve(), 'rb')
		files.append(('file', (file.name, f, 'text/csv')))
		files.append(('data', ('data.json', json.dumps(entity), 'application/json')))
		response = requests.post(self.import_url, files=files, headers=headers)
		# close
		f.close()
		return self.handle_job_response(response)

	def finished(self):
		self.check_status()
		return self.percentage == 100
	
	def check_status(self):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		url = f'https://app.engn.jp/api/v1/deliveries/-/emails/import/{self.job_id}'
		response = requests.get(url, headers=headers)
		json_body = self.handle_error(response)
		self.percentage = json_body['percentage']
		self.status = json_body['status']
		if 'success_count' in json_body.keys():
			self.success_count = json_body['success_count']
		if 'total_count' in json_body.keys():
			self.total_count = json_body['total_count']
		if 'failed_count' in json_body.keys():
			self.failed_count = json_body['failed_count']
		if 'error_file_url' in json_body.keys():
			self.error_file_url = json_body['error_file_url']
		return self.status

	def download_error_file(self, file_path):
		headers = {
			'Authorization': f'Bearer {self.client.token}',
		}
		url = f'https://app.engn.jp/api/v1/deliveries/-/emails/import/{self.job_id}/errorinfo/download'
		response = requests.get(url, headers=headers)
		zip_content = response.content
		f = open(file_path, 'wb')
		f.write(zip_content)
		f.close()
		return True

