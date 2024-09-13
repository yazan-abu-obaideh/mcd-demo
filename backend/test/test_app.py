import json
from http import HTTPStatus
from multiprocessing import Process
from time import sleep

import requests

from mcd_demo.app import build_full_app
from test_utils import McdDemoTestCase


class AppTest(McdDemoTestCase):
    APP_PROCESS: Process

    def setUp(self):
        self.app = build_full_app().test_client()
        self.app.testing = True

    def test_bad_request(self):
        response = self.app.post("/api/v1/optimization/ergonomics/optimize-seeds", data=json.dumps({
            "seedBikeId": "DOES_NOT_EXIST",
            "riderId": "DOES_NOT_EXIST"
        }), headers={"Content-Type": "application/json"})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual("Invalid rider ID [DOES_NOT_EXIST]", response.json["message"])

    def test_not_found(self):
        health_response = self.app.get("/healthy")
        self.assertEqual(HTTPStatus.NOT_FOUND, health_response.status_code)

    def test_health(self):
        health_response = self.app.get("/api/v1/health")
        self.assertEqual("UP", health_response.json["status"])
        self.assertEqual(HTTPStatus.OK, health_response.status_code)
        self.assertEqual("*", health_response.headers["Access-Control-Allow-Origin"])
