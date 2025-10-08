from app import create_app
from app.models import db, Customer
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # Create a default customer for tests that need a pre-existing user
            default_customer = Customer(
                name="Default User",
                email="default@example.com",
                phone="0000000000",
                password="defaultpass"
            )
            db.session.add(default_customer)
            db.session.commit()

    def test_create_customer(self):
        response = self.client.post('/customers/', json={
            "name": "Test User", "email": "test@example.com", "phone": "1234567890", "password": "testpass"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_customer_missing_email(self):
        response = self.client.post('/customers/', json={
            "name": "Test User", "phone": "1234567890", "password": "testpass"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json)

    def test_create_customer_duplicate_email(self):
        # This will conflict with the default customer
        response = self.client.post('/customers/', json={
            "name": "Another User", "email": "default@example.com", "phone": "0987654321", "password": "testpass2"
        })
        self.assertIn(response.status_code, [400, 409])

    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_login_customer(self):
        # Login with the default customer
        response = self.client.post('/customers/login', json={
            "email": "default@example.com", "password": "defaultpass"
        })
        self.assertEqual(response.status_code, 200)

    def test_login_customer_wrong_password(self):
        response = self.client.post('/customers/login', json={
            "email": "default@example.com", "password": "wrong"
        })
        self.assertEqual(response.status_code, 401)

    def test_get_customer(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/999')
        self.assertEqual(response.status_code, 404)

    def test_patch_customer(self):
        response = self.client.patch('/customers/1', json={"name": "Updated"})
        self.assertIn(response.status_code, [200, 204])

    def test_patch_customer_not_found(self):
        response = self.client.patch('/customers/999', json={"name": "Updated"})
        self.assertEqual(response.status_code, 404)

    def test_delete_customer(self):
        response = self.client.delete('/customers/1')
        self.assertIn(response.status_code, [200, 204])

    def test_delete_customer_not_found(self):
        response = self.client.delete('/customers/999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
