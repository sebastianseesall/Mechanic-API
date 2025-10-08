from app import create_app
from app.models import db, Mechanic
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            default_mechanic = Mechanic( #pre-existing mechanic for tests that need it
                first_name="Default",
                last_name="Mechanic",
                email="mechanic@example.com"
            )
            db.session.add(default_mechanic)
            db.session.commit()

    def test_create_mechanic(self):
        response = self.client.post('/mechanics/', json={
            "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_mechanic_missing_email(self):
        response = self.client.post('/mechanics/', json={
            "first_name": "Jane", "last_name": "Doe"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)

    def test_create_mechanic_duplicate_email(self):
        self.client.post('/mechanics/', json={
            "first_name": "Jane", "last_name": "Doe", "email": "dup@example.com"
        })
        response = self.client.post('/mechanics/', json={
            "first_name": "Janet", "last_name": "Smith", "email": "dup@example.com"
        })
        self.assertIn(response.status_code, [400, 409])

    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    def test_get_mechanic(self):
        self.client.post('/mechanics/', json={
            "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"
        })
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)

    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_patch_mechanic(self):
        self.client.post('/mechanics/', json={
            "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"
        })
        response = self.client.patch('/mechanics/1', json={"first_name": "Janet"})
        self.assertIn(response.status_code, [200, 204])

    def test_patch_mechanic_not_found(self):
        response = self.client.patch('/mechanics/999', json={"first_name": "Janet"})
        self.assertEqual(response.status_code, 404)

    def test_delete_mechanic(self):
        self.client.post('/mechanics/', json={
            "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com"
        })
        response = self.client.delete('/mechanics/1')
        self.assertIn(response.status_code, [200, 204])

    def test_delete_mechanic_not_found(self):
        response = self.client.delete('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_ranked_mechanics(self):
        response = self.client.get('/mechanics/ranked')
        self.assertEqual(response.status_code, 200)

    def test_search_mechanics(self):
        response = self.client.get('/mechanics/search?name=Jane')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()