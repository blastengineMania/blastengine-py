from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import unittest
from blastengine.Mail import Mail
from blastengine.Transaction import Transaction
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
		mail.subject('テストメール transaction')
		mail.text_part('テストメールです。 __name1__')
		mail.to(f'be@moongift.co.jp', {
			'name1': f'Name 1',
		})
		mail.encode('UTF-8')
		delivery_id = mail.send()
		self.assertIsNotNone(delivery_id)

	def test_send_transaction(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		transaction = Transaction()
		transaction.subject('test mail')
		transaction.text_part('mail body')
		transaction.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		transaction.to(f'be@moongift.co.jp')
		delivery_id = transaction.send()
		self.assertIsNotNone(delivery_id)

	def test_send_transaction_with_cc(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		transaction = Transaction()
		transaction.subject('test mail with cc')
		transaction.text_part('mail body')
		transaction.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		transaction.to(f'be@moongift.co.jp')
		transaction.cc(f'be2@moongift.co.jp')
		delivery_id = transaction.send()
		self.assertIsNotNone(delivery_id)

	def test_send_with_attachment(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.subject('テストメール transaction with attachment')
		mail.text_part('テストメールです。 __name1__')
		mail.attachments(join(dirname(__file__), '../README.md'))
		mail.to(f'be@moongift.co.jp', {
			'name1': f'Name 1',
		})
		mail.encode('UTF-8')
		delivery_id = mail.send()
		self.assertIsNotNone(delivery_id)

if __name__ == '__main__':
  unittest.main()