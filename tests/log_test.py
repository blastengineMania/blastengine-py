from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
import unittest
from blastengine.Log import Log
from blastengine.Client import Blastengine
import os
from os.path import join, dirname
from dotenv import load_dotenv

class TestMail(unittest.TestCase):
	def test_fetch(self):
		load_dotenv(verbose=True)
		Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		ary = Log.fetch()
		print(ary[0])
		print(ary[0].id)
		print(ary[0].delivery_type)

	def test_fetch2(self):
		load_dotenv(verbose=True)
		Blastengine(os.environ.get("USER_ID"), os.environ.get("API_KEY"))
		ary = Log.fetch({
			'status': ['EDIT', 'SOFTERROR'],
			'count': 2,
			'anchor': 4582,
		})
		print(ary[0].id)
		print(ary[0].last_response_code)
		print(ary[0].status)
		print(ary[1].id)
		print(ary[1].last_response_code)
		print(ary[1].status)
if __name__ == '__main__':
  unittest.main()