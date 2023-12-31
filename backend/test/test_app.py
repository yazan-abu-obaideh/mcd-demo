import json
from http import HTTPStatus
from multiprocessing import Process
from time import sleep

import requests

from app import build_full_app
from test_utils import McdDemoTestCase


class AppTest(McdDemoTestCase):
    APP_PROCESS: Process

    @classmethod
    def setUpClass(cls) -> None:
        cls.APP_PROCESS = Process(target=lambda: build_full_app().run(port=5000))
        cls.APP_PROCESS.start()
        cls.await_app()
        cls.handle_timeout()

    @classmethod
    def await_app(cls):
        sleep(0.1)

    def test_bad_request(self):
        response = requests.post(self.build_end_point("/optimization/ergonomics/optimize-seeds"), data=json.dumps({
            "seedBikeId": "DOES_NOT_EXIST",
            "riderId": "DOES_NOT_EXIST"
        }), headers={"Content-Type": "application/json"})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual("Invalid rider ID [DOES_NOT_EXIST]", response.json()["message"])

    def test_not_found(self):
        health_response = requests.get(self.build_end_point("/healthy"))
        self.assertEqual(HTTPStatus.NOT_FOUND, health_response.status_code)

    def test_health(self):
        health_response = requests.get(self.build_end_point("/health"))
        self.assertEqual("UP", health_response.json()["status"])
        self.assertEqual(HTTPStatus.OK, health_response.status_code)
        self.assertEqual("*", health_response.headers["Access-Control-Allow-Origin"])

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
        return requests.get(AppTest.build_end_point("/health"))

    @staticmethod
    def build_end_point(suffix):
        return f"http://localhost:5000/api/v1{suffix}"
