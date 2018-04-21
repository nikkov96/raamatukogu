import json
import unittest

from app import app
app.testing = True


class TestApi(unittest.TestCase):
    def test_home_status_code(self):
        with app.test_client() as client:
            result = client.get('/')
            self.assertEqual(result.status_code, 200)

    def test_add_order(self):
        with app.test_client() as client:
            sending = {'kood': 1, 'nimi': 'test', 'email': 'test@test.com', 'telefon':55555, 'isikukood':55555}
            result = client.post(
                '/order',
                data=sending
            )

            self.assertEqual(
                json.loads(result.data),
                json.loads(json.dumps({'message': 'Order created successfully!'}))
            )

    def test_finish_order(self):
        with app.test_client() as client:
            sending = {'kood': 1, 'telefon':55555, 'isikukood':55555}
            result = client.post(
                '/tagasta',
                data=sending
            )

            self.assertEqual(
                json.loads(result.data),
                json.loads(json.dumps({'message': 'Book returned successfully!'}))
            )