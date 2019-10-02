from app import app
import unittest
import json
from pydblite import Base
import os

class PetsTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        test_db = 'test_pets.pdl'
        if os.path.exists(test_db):
            os.remove(test_db)
        self.app.application.db = Base(test_db)
        self.app.application.db.create('name', 'type', 'age', 'sex', 'description', 'owner_email', 'image_url')
        self.test_create_pets()


    def test_create_pets(self):
        pets_to_create = _initial_pets()
        result = self.app.post('/pet', data=json.dumps(pets_to_create), content_type='application/json')
        pets_created = json.loads(result.data.decode('utf8'))

        assert len(pets_created) == len(pets_to_create)


    def test_update_pets(self):
        new_name = 'Rover Jr.'
        pets_to_update = [{'id': 0, 'name': new_name}]
        self.app.put('/pet', data=json.dumps(pets_to_update), content_type='application/json')

        updated_pet = self.app.application.db[pets_to_update[0]['id']]

        assert updated_pet is not None

        assert updated_pet['id'] == pets_to_update[0]['id']

        original_record = _initial_pets()[0]

        assert updated_pet['type'] == original_record['type']
        assert updated_pet['age'] == original_record['age']
        assert updated_pet['sex'] == original_record['sex']
        assert updated_pet['description'] == original_record['description']
        assert updated_pet['owner_email'] == original_record['owner_email']
        assert updated_pet['image_url'] == original_record['image_url']


    def test_delete_pets(self):
        pets_to_delete = [0,1]
        self.app.delete('/pet', data=json.dumps(pets_to_delete), content_type='application/json')
        records_left = self.app.application.db

        assert len(records_left) == len(_initial_pets()) - len(pets_to_delete)


    def test_get_pets(self):
        filters = {'age': 10, 'sex': 'f'}
        result = self.app.get('/pet', data=json.dumps(filters), content_type='application/json')

        records = json.loads(result.data.decode('utf8'))

        assert len(records) == 1


def _initial_pets():
    return [{
            "name": "Rover",
            "type": "Dog",
            "age": 3,
            "sex": "m",
            "description": "Schnauzer",
            "owner_email": "bob.smith@mail.com",
            "image_url": "www.example.com"

        },
        {
            "name": "Slowpoke",
            "type": "Turtle",
            "age": 30,
            "sex": "m",
            "description": "Green",
            "owner_email": "esther.jones@mail.com",
            "image_url": "www.example.com"

        },
        {
            "name": "Tweety",
            "type": "Bird",
            "age": 10,
            "sex": "f",
            "description": "Parrot",
            "owner_email": "alice.park@mail.com",
            "image_url": "www.example.com"

        }]


if __name__ == "__main__":
        unittest.main()
