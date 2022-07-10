class MailBase:
	clinet = None

	def __init__(self):
		self._subject = ''
		self._to = []
		self._cc = []
		self._bcc = []
		self._from = {}
		self._encode = 'UTF-8'
		self._insert_code = None
		self._text_part = ''
		self._html_part = None

	def subject(self, value):
		self._subject = value
	
	def to(self, email):
		self._to.append(email)
	
	def cc(self, email):
		self._cc.append(email)
	
	def bcc(self, email):
		self._bcc.append(email)
	
	def fromAddress(self, email, name = ''):
		self._from = {
			'email': email,
			'name': name
		}
	
	def insert_code(key, value):
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
