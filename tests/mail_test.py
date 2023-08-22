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
	def test_fetch(self):
		load_dotenv(verbose=True)
		client = Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		ary = Mail.fetch()
		print(ary[0])
		print(ary[0].subject())
		print(ary[0].from_address())
if __name__ == '__main__':
  unittest.main()