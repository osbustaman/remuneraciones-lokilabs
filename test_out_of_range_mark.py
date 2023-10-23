import requests
import unittest

class TestOutOfRangeMark(unittest.TestCase):
    def test_out_of_range_mark(self):
        # Define la URL del endpoint que deseas probar
        url = "http://osbustaman.lokilabs.local:8080/api/attendance/in-and-out/"

        # Define los datos a enviar en la solicitud POST
        data = {
            'user': '17452821-7',
            'ma_typeattendance': 1,
            'ma_latitude': '-33.43476615714285',
            'ma_longitude': '-70.68733879999999',
            'ma_modeldevice': 'Iphone 12',
            'ma_photo': 'String en base64',
            'ma_typemark': 1,  # MOVIL
            'ma_platformmark': 'navegador de internet en el caso que la marca sea desde la web',
            'ma_datemark': '2023-10-03',  # Fecha en formato YYYY-mm-dd
        }

        # Define el token Bearer
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE5NTUzNDc0LCJpYXQiOjE2OTc5NTM0NzQsImp0aSI6IjQ4YjI5YzAxMDVhNTQ3NWRiMGMwZDg4N2E5OTkzYzFhIiwidXNlcl9pZCI6Mn0.YZ5aFqMtbXnQfQc4L7DugE1xuQr_07K9vOdtneqfbyg'

        # Define el encabezado de autorización
        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Realiza la solicitud POST con los datos y el encabezado
        response = requests.post(url, json=data, headers=headers)

        # Verifica la respuesta, por ejemplo:
        self.assertEqual(response.status_code, 500)  # Espera una respuesta de código 500
        print(response.request)
        print(response.status_code)

if __name__ == '__main__':
    unittest.main()
