import base64
import json
import unittest
from http import HTTPStatus
from multiprocessing import Process
from time import sleep

import requests

from optimization_app import app
from test_utils import McdDemoTestCase


class AppTest(McdDemoTestCase):
    APP_PROCESS: Process

    @classmethod
    def setUpClass(cls) -> None:
        cls.APP_PROCESS = Process(target=app.run)
        cls.APP_PROCESS.start()
        cls.handle_timeout()

    def test_bad_request(self):
        with open(self.resource_path("dude.jpeg"), "rb") as file:
            response = requests.post(self.build_end_point("/ergonomics/optimize-custom-rider"), data=json.dumps({
                "seedBikeId": "DOES_NOT_EXIST",
                "imageBase64": b"",
                "cameraHeight": 45,
                "personHeight": 45
            }), headers={"Content-Type": "application/json"})
            self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
            self.assertEqual("Invalid seed bike ID", response.json()["message"])

    def test_not_found(self):
        health_response = requests.get(self.build_end_point("healthy"))
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
