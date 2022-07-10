from blastengine.MailBase import MailBase
import requests
import json

class Transaction(MailBase):

	def send(self):
		url = 'https://app.engn.jp/api/v1/deliveries/transaction'
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
		headers = {
			'Authorization': f'Bearer {self.client.token}',
			'content-type': 'application/json'
		}
		response = requests.post(url, data=json.dumps(entity), headers=headers)
		json_body = json.loads(response.content)
		if response.status_code > 300:
			messages = []
			for key in json_body['error_messages']:
				messages.append(f"{key}: {', '.join(json_body['error_messages'][key])}")
			raise Exception("\n".join(messages))
		return json_body['delivery_id']