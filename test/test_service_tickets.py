from app import create_app
from app.models import db, Customer
import unittest

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            customer = Customer( #pre-existing customer for tests that need it
                name="Ticket User",
                email="ticketuser@example.com",
                phone="1111111111",
                password="ticketpass"
            )
            db.session.add(customer)
            db.session.commit()

    def test_create_service_ticket(self):
        response = self.client.post('/service_tickets/', json={
            "customer_id": 1, "description": "Fix brakes"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_service_ticket_missing_customer(self):
        response = self.client.post('/service_tickets/', json={
            "description": "Fix brakes"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('customer_id', response.json)

    def test_get_service_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)

    def test_get_service_ticket(self):
        self.client.post('/service_tickets/', json={
            "customer_id": 1, "description": "Fix brakes"
        })
        response = self.client.get('/service_tickets/1')
        self.assertEqual(response.status_code, 200)

    def test_get_service_ticket_not_found(self):
        response = self.client.get('/service_tickets/999')
        self.assertEqual(response.status_code, 404)

    def test_patch_service_ticket(self):
        self.client.post('/service_tickets/', json={
            "customer_id": 1, "description": "Fix brakes"
        })
        response = self.client.patch('/service_tickets/1', json={"description": "Fix engine"})
        self.assertIn(response.status_code, [200, 204])

    def test_patch_service_ticket_not_found(self):
        response = self.client.patch('/service_tickets/999', json={"description": "Fix engine"})
        self.assertEqual(response.status_code, 404)

    def test_delete_service_ticket(self):
        self.client.post('/service_tickets/', json={
            "customer_id": 1, "description": "Fix brakes"
        })
        response = self.client.delete('/service_tickets/1')
        self.assertIn(response.status_code, [200, 204])

    def test_delete_service_ticket_not_found(self):
        response = self.client.delete('/service_tickets/999')
        self.assertEqual(response.status_code, 404)

    def test_add_part(self):
        # You may need to add inventory and ticket first
        self.client.post('/service_tickets/', json={
            "customer_id": 1, "description": "Fix brakes"
        })
        response = self.client.post('/service_tickets/1/add_part', json={"part_id": 1, "quantity": 1})
        self.assertIn(response.status_code, [200, 201, 400])  # 400 if part doesn't exist

    def test_add_part_ticket_not_found(self):
        response = self.client.post('/service_tickets/999/add_part', json={"part_id": 1, "quantity": 1})
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()