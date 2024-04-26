
from rest_framework.test import APITestCase
from .models import Rick
from django.urls import reverse
from rest_framework import status
# from .serializers import RickSerializer


class RickTestCase(APITestCase):
    """
        Test for CRUD functionalities for the 'ricks' endpoint
    """

    def test_get_all_ricks(self):
        Rick.objects.create(universe="t380", is_morty_alive=True)
        Rick.objects.create(universe="t490", is_morty_alive=False)
        response = self.client.get(reverse('ricks-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_one_rick(self):
        new_rick = Rick.objects.create(universe="t380", is_morty_alive=True)
        response = self.client.get(reverse('ricks-detail', args=(new_rick.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": new_rick.id,
            "universe": new_rick.universe,
            "is_morty_alive": new_rick.is_morty_alive
            })

    def test_get_one_rick_non_existent_id(self):
        new_rick = Rick.objects.create(universe="t380", is_morty_alive=True)
        response = self.client.get(reverse('ricks-detail', args=(new_rick.id+1,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_one_rick(self):
        self.assertFalse(Rick.objects.filter(universe="t590").exists())
        data = {
            "universe": "t590",
            "is_morty_alive": False
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Rick.objects.filter(universe="t590").exists())

    def test_create_one_rick_no_data(self):
        data = None
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_rick_missing_field_data(self):
        data = {
            "universe": "",
            "is_morty_alive": False
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_rick(self):
        new_rick = Rick.objects.create(universe="t380", is_morty_alive=True)
        self.assertFalse(Rick.objects.filter(universe="t390").exists())
        data = {
            "universe": "t390",
            "is_morty_alive": False
        }
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Rick.objects.filter(universe="t390").exists())

    def test_update_one_rick_no_data(self):
        new_rick = Rick.objects.create(universe="t380", is_morty_alive=True)
        data = {
            "universe": "",
            "is_morty_alive": False
        }
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_rick_missing_field_data(self):
        new_rick = Rick.objects.create(universe="t380", is_morty_alive=True)
        data = {
            "universe": "",
            "is_morty_alive": False
        }
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_rick_non_existent_id(self):
        new_rick = Rick.objects.create(universe="t380", is_morty_alive=True)
        self.assertFalse(Rick.objects.filter(universe="t390").exists())
        data = {
            "universe": "t390",
            "is_morty_alive": False
        }
        response = self.client.put(reverse('ricks-detail', args=(new_rick.id+1,)), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_one_rick(self):
        new_rick = Rick.objects.create(universe="t590", is_morty_alive=True)
        self.assertTrue(Rick.objects.filter(universe="t590").exists())

        response = self.client.delete(reverse('ricks-detail', args=(new_rick.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Rick.objects.filter(universe="t590").exists())

    def test_delete_one_rick_non_existent_id(self):
        new_rick = Rick.objects.create(universe="t590", is_morty_alive=True)
        self.assertTrue(Rick.objects.filter(universe="t590").exists())

        response = self.client.delete(reverse('ricks-detail', args=(new_rick.id+1,)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
