import unittest
from multiprocessing import Process
from time import sleep

import requests

from backend.app import app


class AppTest(unittest.TestCase):
    APP_PROCESS: Process

    @classmethod
    def setUpClass(cls) -> None:
        cls.APP_PROCESS = Process(target=app.run)
        cls.APP_PROCESS.start()
        cls.handle_timeout()

    def test_stall(self):
        while True:
            print("stalling...")
            sleep(10)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.APP_PROCESS.terminate()

    @classmethod
    def handle_timeout(cls):
        attempts = 0
        while cls.get_health().status_code != 200:
            sleep(1)
            attempts += 1
            if attempts > 5:
                raise AssertionError("Timed out waiting for app to run")
        print("App running...")

    @classmethod
    def get_health(cls):
        return requests.get("http://localhost:5000/health")
