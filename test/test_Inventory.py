from app import create_app
from app.models import Inventory, db
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            part = Inventory( #pre-existing part for tests that need it
                part_name="Default Part",
                part_number="DP001",
                quantity_in_stock=10,
                price=9.99
            )
            db.session.add(part)
            db.session.commit()

    def test_create_inventory(self):
        response = self.client.post('/inventory/', json={
            "part_name": "Brake Pad", "part_number": "BP123", "quantity_in_stock": 10, "price": 19.99
        })
        self.assertEqual(response.status_code, 201)

    def test_create_inventory_missing_name(self):
        response = self.client.post('/inventory/', json={
            "part_number": "BP123", "quantity_in_stock": 10, "price": 19.99
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('part_name', response.json)

    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)

    def test_get_inventory_part(self):
        self.client.post('/inventory/', json={
            "part_name": "Brake Pad", "part_number": "BP123", "quantity_in_stock": 10, "price": 19.99
        })
        response = self.client.get('/inventory/1')
        self.assertEqual(response.status_code, 200)

    def test_get_inventory_part_not_found(self):
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)

    def test_patch_inventory(self):
        self.client.post('/inventory/', json={
            "part_name": "Brake Pad", "part_number": "BP123", "quantity_in_stock": 10, "price": 19.99
        })
        response = self.client.patch('/inventory/1', json={"quantity_in_stock": 5})
        self.assertIn(response.status_code, [200, 204])

    def test_patch_inventory_not_found(self):
        response = self.client.patch('/inventory/999', json={"quantity_in_stock": 5})
        self.assertEqual(response.status_code, 404)

    def test_delete_inventory(self):
        self.client.post('/inventory/', json={
            "part_name": "Brake Pad", "part_number": "BP123", "quantity_in_stock": 10, "price": 19.99
        })
        response = self.client.delete('/inventory/1')
        self.assertIn(response.status_code, [200, 204])

    def test_delete_inventory_not_found(self):
        response = self.client.delete('/inventory/999')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()