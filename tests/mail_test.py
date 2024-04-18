from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import unittest
from blastengine.Mail import Mail
from blastengine.Client import Blastengine
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime

class TestMail(unittest.TestCase):
	def test_find(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		ary = Mail.find({
			"limit": 1,
			"delivery_type": ["BULK"],
			"list_unsubscribe_mailto": "moongift"
		})
		print(ary[0])
		print(ary[0].subject())
		print(ary[0].from_address())
	def test_all(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		ary = Mail.all({
			"limit": 1,
			"delivery_type": ["BULK"],
		})
		print(ary[0])
		print(ary[0].subject())
		print(ary[0].from_address())
	def test_send_transaction_mail(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.subject('メールの件名')
		mail.text_part('テキスト本文 __name__')
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.to('atsushi+1@moongift.co.jp', {'name': 'name 1', 'hash': 'aaaaa'})
		mail.to('atsushi+2@moongift.co.jp', {'name': 'name 2', 'hash': 'bbbbb'})
		mail.unsubscribe(url='https://example.com/unsubscribe/__hash__', email='unsubscrie+__hash__@example.com')
		delivery_id = mail.send()
		print(delivery_id)
	def test_send_transaction_mail_only_url(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.subject('メールの件名 unsubscribe only url')
		mail.text_part('テキスト本文 __name__')
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.to('atsushi+1@moongift.co.jp', {'name': 'name 1', 'hash': 'aaaaa'})
		mail.to('atsushi+2@moongift.co.jp', {'name': 'name 2', 'hash': 'bbbbb'})
		mail.unsubscribe(url='https://example.com/unsubscribe/__hash__')
		delivery_id = mail.send()
		print(delivery_id)
	def test_send_transaction_mail_only_email(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.subject('メールの件名 unsubscribe only email')
		mail.text_part('テキスト本文 __name__')
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.to('atsushi+1@moongift.co.jp', {'name': 'name 1', 'hash': 'aaaaa'})
		mail.unsubscribe(email='unsubscrie+__hash__@example.com')
		delivery_id = mail.send()
		print(delivery_id)
	def test_cancel_mail(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		mail = Mail()
		mail.subject('メールの件名 unsubscribe only email')
		mail.text_part('テキスト本文 __name__')
		mail.from_address(os.environ.get("FROM_EMAIL"), os.environ.get("FROM_NAME"))
		mail.to('atsushi+1@moongift.co.jp', {'name': 'name 1', 'hash': 'aaaaa'})
		# make datetime 30 sec later now
		dt = datetime.datetime.now() + datetime.timedelta(seconds=30)
		delivery_id = mail.send(dt)
		print(delivery_id)
		mail.get()
		print(mail.status)
		mail.cancel()
		mail.get()
		print(mail.status)
if __name__ == '__main__':
  unittest.main()