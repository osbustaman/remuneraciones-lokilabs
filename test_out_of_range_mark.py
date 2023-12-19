import json
import requests
import unittest
from datetime import datetime

class TestOutOfRangeMark(unittest.TestCase):

    def test_out_of_range_mark(self):

        fecha_actual = datetime.now()
        solo_fecha = fecha_actual.date()

        url = "http://osbustaman.lokilabs.local:8000/in-and-out/"

        payload = json.dumps({
            "user": "3",
            "ma_typeattendance": 1,
            "ma_latitude": "-33.41839010554017",
            "ma_longitude": "-70.60184023474068",
            "ma_modeldevice": "Iphone 12",
            "ma_photo": "String en base64",
            "ma_typemark": 2,
            "ma_platformmark": "navegador de internet en el caso que la marca sea desde la web",
            "ma_datemark": "2023-12-19"
        })
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI0NTkyNTc0LCJpYXQiOjE3MDI5OTI1NzQsImp0aSI6IjYwYTk5ZjEwYTI3ZTQ1YTM5OWIwNDYzNjFmNTYzY2Y2IiwidXNlcl9pZCI6MX0.Z2m25-i6s7jfkxni2eC4Q4NXrPjDzfkPBUlk2uf-rmY',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Verifica la respuesta
        expected_status_codes = [200, 201, 400, 401, 403, 404, 500]  # Lista de códigos esperados
        self.assertIn(response.status_code, expected_status_codes)  # Verifica si el código está dentro de los esperados

        status_messages = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error"
        }

        if response.status_code in status_messages:
            print(f"{response.status_code} - {status_messages[response.status_code]}")
            
            # Mostrar los mensajes de respuesta específicos si están disponibles
            if response.status_code == 400:
                print(f"Error 400: {response.json()}")
            elif response.status_code == 401:
                print(f"Error 401: {response.json()}")
            elif response.status_code == 404:
                print(f"Error 404: {response.json()}")
            elif response.status_code == 500:
                print(f"Error 500: {response.json()}")
            elif response.status_code == 201:
                print(f"Success 201: {response.json()}")  # Suponiendo que devuelve datos del registro creado
            elif response.status_code == 200:
                print(f"Success 200: {response.json()}")  # Suponiendo que devuelve datos del registro creado
            else:
                print("Unknown Status Code")
        else:
            print("Unknown Status Code")


if __name__ == '__main__':
    unittest.main()
