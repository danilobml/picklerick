
from rest_framework.test import APITestCase
from .models import Rick
from morties.models import Morty
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class RickTestCase(APITestCase):
    """
        Test for CRUD functionalities for the 'ricks' endpoint
    """

    client = APIClient()

    def setUp(self):
        User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")

    def test_get_all_ricks(self):
        Rick.objects.create(universe="t380")
        Rick.objects.create(universe="t490")
        response = self.client.get(reverse('ricks-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_one_rick(self):
        new_rick = Rick.objects.create(universe="t380")
        response = self.client.get(reverse('ricks-detail', args=(new_rick.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": new_rick.id,
            "universe": new_rick.universe,
            "paired_morties": [],
            "user": None
            })

    def test_get_one_rick_with_all_paired_morties(self):
        new_rick = Rick.objects.create(universe="t380")
        paired_morty1 = Morty.objects.create(universe="t380", is_alive=True, paired_rick=new_rick)
        paired_morty2 = Morty.objects.create(universe="t460", is_alive=False, paired_rick=new_rick)
        response = self.client.get(reverse('ricks-detail', args=(new_rick.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": new_rick.id,
            "universe": new_rick.universe,
            "paired_morties": [
                {
                    "id": paired_morty1.id,
                    "universe": paired_morty1.universe,
                    "is_alive": paired_morty1.is_alive,
                    "paired_rick": new_rick.id
                },
                {
                    "id": paired_morty2.id,
                    "universe": paired_morty2.universe,
                    "is_alive": paired_morty2.is_alive,
                    "paired_rick": new_rick.id
                }],
            "user": None
            })

    def test_get_one_rick_non_existent_id(self):
        response = self.client.get(reverse('ricks-detail', args=(5,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_one_rick(self):
        created_universe = "t590"
        self.assertFalse(Rick.objects.filter(universe=created_universe).exists())
        data = {
            "universe": created_universe,
            "username": "testuser",
            "password": "testpass"
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Rick.objects.filter(universe=created_universe).exists())

    def test_create_one_rick_already_existent_universe(self):
        existing_universe = "t590"
        Rick.objects.create(universe=existing_universe)
        data = {
            "universe": existing_universe
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_rick_no_data(self):
        data = None
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_rick_missing_universe_data(self):
        data = {
            "universe": "",
            "username": "testuser",
            "password": "testpass"
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_rick_missing_username_data(self):
        data = {
            "universe": "s350",
            "username": "",
            "password": "testpass"

        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_rick_missing_password_data(self):
        data = {
            "universe": "s350",
            "username": "testuser",
            "password": ""
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ricks_universe(self):
        modified_universe = "t390"
        new_rick = Rick.objects.create(universe="t380")
        self.assertFalse(Rick.objects.filter(universe=modified_universe).exists())
        data = {
            "universe": modified_universe
        }
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_rick_no_data(self):
        new_rick = Rick.objects.create(universe="t380")
        data = None
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_rick_missing_field_data(self):
        new_rick = Rick.objects.create(universe="t380")
        data = {
            "universe": ""
        }
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_rick_non_existent_id(self):
        data = {
            "universe": "t390"
        }
        response = self.client.put(reverse('ricks-detail', args=(5,)), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_one_rick(self):
        checked_universe = "t590"
        new_rick = Rick.objects.create(universe=checked_universe)
        self.assertTrue(Rick.objects.filter(universe=checked_universe).exists())

        response = self.client.delete(reverse('ricks-detail', args=(new_rick.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Rick.objects.filter(universe="t590").exists())

    def test_delete_one_rick_non_existent_id(self):
        response = self.client.delete(reverse('ricks-detail', args=(5,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unlogged_user(self):
        self.client.logout()
        response = self.client.get(reverse("ricks-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
