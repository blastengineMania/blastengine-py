import re
from blastengine.MailBase import MailBase
from blastengine.Transaction import Transaction
from blastengine.Bulk import Bulk
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode

class Mail(MailBase):
	@classmethod
	def _find(cls, path, params = {}):
		headers = {
			'Authorization': f'Bearer {cls.client.token}',
			'content-type': 'application/json'
		}
		querystring = urlencode(params)
		response = requests.get(f'{cls.endpoint_url}{path}?{querystring}', headers=headers)
		json_body = cls.handle_array_response(response)
		res = []
		for params in json_body:
			mail = Transaction() if params['delivery_type'] == 'TRANSACTION' else Bulk()
			mail.sets(params)
			res.append(mail)
		return res
	@classmethod
	def find(cls, params = {}):
		return cls._find('/deliveries', params)
	@classmethod
	def all(cls, params = {}):
		return cls._find('/deliveries/all', params)
	
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

	def send(self, date = None):
		if len(self._cc) > 0 or len(self._bcc) > 0:
			if date is not None:
				raise Exception('You can not specify the date when sending CC or BCC.')
			if len(self._to) > 1:
				raise Exception('You can not specify the to when sending CC or BCC.')
		if date is not None or len(self._to) == 1:
			return self.send_transaction_mail()
		return self.send_bulk_mail()

	def send_transaction_mail(self):
		transaction = Transaction()
		self.generate_base(transaction)
		params = self._to[0]
		transaction.to(params['email'])
		if len(params['insert_code']) > 0:
			for insert_code in params['insert_code']:
				transaction.insert_code(insert_code['key'], insert_code['value'])
		if len(self._cc) > 0:
			for cc in self._cc:
				transaction.cc(cc)
		if len(self._bcc) > 0:
			for bcc in self._bcc:
				transaction.bcc(bcc)
		transaction.send()
		return transaction.delivery_id

	def send_bulk_mail(self):
		bulk = Bulk()
		self.generate_base(bulk)
		if len(self._to) > 0:
			for params in self._to:
				data = {}
				for insert_code in params['insert_code']:
					data[re.sub('__(.*)__', '\\1', insert_code['key'])] = insert_code['value']
				bulk.to(params['email'], data)
		bulk.begin()
		bulk.update()
		bulk.send()
		return bulk.delivery_id
	
	def generate_base(self, base):
		base.subject(self._subject)
		base.from_address(self._from['email'], self._from['name'])
		base.text_part(self._text_part)
		if self._html_part is not None:
			base.html_part(self._html_part)
		if self._unsubscribe is not None:
			unsubscribe = {}
			if 'url' in self._unsubscribe:
				unsubscribe['url'] = self._unsubscribe['url']
			else:
				unsubscribe['url'] = None
			if 'email' in self._unsubscribe:
				unsubscribe['email'] = self._unsubscribe['email']
			else:
				unsubscribe['email'] = None
			base.unsubscribe(url=unsubscribe['url'], email=unsubscribe['email'])
		if self._encode is not None:
			base.encode(self._encode)
		if len(self._attachments) > 0:
			for attachment in self._attachments:
				base.attachments(attachment)
		return base
