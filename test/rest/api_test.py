import http.client
import os
import unittest
from urllib.request import urlopen
from urllib.error import HTTPError
# Importo la librería "Threading" para controlar la race condition
import threading

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 10  # in secs
# Defino un bloqueo para la URL
url_lock = threading.Lock()

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        with url_lock:
            self.assertIsNotNone(BASE_URL, "URL no configurada")
            self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        with url_lock:
            url = f"{BASE_URL}/calc/add/1/2"
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            try:
                self.assertEqual(
                    response.status, http.client.OK, f"Error en la petición API a {url}"
                )
                self.assertEqual(
                    response.read().decode(), "3", "ERROR ADD"
                )
            finally:
                response.close()

    def test_api_multiply(self):
        with url_lock:
            url = f"{BASE_URL}/calc/multiply/2/2"
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            try:
                self.assertEqual(
                    response.status, http.client.OK, f"Error en la petición API a {url}"
                )
                self.assertEqual(
                    response.read().decode(), "4", "ERROR MULTIPLY"
                )
            finally:
                response.close()

    def test_api_divide(self):
        with url_lock:
            url = f"{BASE_URL}/calc/divide/2/2"
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            try:
                self.assertEqual(
                    response.status, http.client.OK, f"Error en la petición API a {url}"
                )
                self.assertEqual(
                    response.read().decode(), "1.0", "ERROR DIVIDE"
                )
            finally:
                response.close()

    def test_api_divide_0(self):
        with url_lock:
            url = f"{BASE_URL}/calc/divide/4/0"
            try:
                response0 = urlopen(url, timeout=DEFAULT_TIMEOUT)
            except HTTPError as e:
                self.assertEqual(
                    e.code, http.client.NOT_ACCEPTABLE, f"Error en la petición API a {url}"
                )
                self.assertEqual(
                    e.read().decode(), "Error: No se puede dividir por 0", "ERROR DIVIDE"
                )
            # Ya que esta conexión nunca se llega a abrir, dado el fallo obligado por el test, no es necesario cerrar la conexión.

    def test_api_sqrt(self):
        with url_lock:
            url = f"{BASE_URL_MOCK}/calc/sqrt/64"
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            try:
                self.assertEqual(
                    response.status, http.client.OK, f"Error en la petición API a {url}"
                )
                self.assertEqual(
                    response.read().decode(), "8", "ERROR SQRT"
                )
            finally:
                response.close()

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
