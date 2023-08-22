from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import unittest
from blastengine.Mail import Mail
from blastengine.Client import Blastengine
import os
from os.path import join, dirname
from dotenv import load_dotenv

class TestMail(unittest.TestCase):
	def test_send(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.subject('テストメール')
		mail.text_part('テストメールです。 __name1__')
		for i in range(55):
			mail.to(f'be{i}@moongift.co.jp', {
				'name1': f'Name {i}',
			})
		mail.encode('UTF-8')
		delivery_id = mail.send()
		self.assertIsNotNone(delivery_id)
	def test_send_with_attachment(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.subject('テストメール with attachment')
		mail.text_part('テストメールです。 __name1__')
		mail.attachments(join(dirname(__file__), '../README.md'))
		for i in range(55):
			mail.to(f'be{i}@moongift.co.jp', {
				'name1': f'Name {i}',
			})
		mail.encode('UTF-8')
		delivery_id = mail.send()
		self.assertIsNotNone(delivery_id)
if __name__ == '__main__':
  unittest.main()