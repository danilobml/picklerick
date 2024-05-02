from rest_framework.test import APITestCase
from .models import Morty
from ricks.models import Rick
from django.urls import reverse
from rest_framework import status
import json


class MortyTestCase(APITestCase):
    """
        Test for CRUD functionalities for the 'morties' endpoint
    """

    def tearDown(self):
        Morty.objects.all().delete()

    def test_get_all_morties(self):
        Morty.objects.create(universe="t380")
        Morty.objects.create(universe="t490", is_alive=False)
        response = self.client.get(reverse('morties-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_one_morty(self):
        new_morty = Morty.objects.create(universe="t380")
        response = self.client.get(reverse('morties-detail', args=(new_morty.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": new_morty.id,
            "universe": new_morty.universe,
            "is_alive": new_morty.is_alive,
            "paired_rick": None
            })

    def test_get_one_morty_non_existent_id(self):
        response = self.client.get(reverse('morties-detail', args=(5,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_one_morty(self):
        created_universe = "t590"
        self.assertFalse(Morty.objects.filter(universe=created_universe).exists())
        data = {
            "universe": created_universe
        }
        response = self.client.post(reverse('morties-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Morty.objects.filter(universe=created_universe).exists())

    def test_create_one_morty_default_is_alive(self):
        created_universe = "t650"
        self.assertFalse(Morty.objects.filter(universe=created_universe).exists())
        data = {
            "universe": created_universe
        }
        response = self.client.post(reverse('morties-list'), data=json.dumps(data), content_type='application/json')
        new_morty = Morty.objects.get(universe=created_universe)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Morty.objects.filter(universe=created_universe).exists())
        self.assertTrue(new_morty.is_alive)

    def test_create_one_morty_already_existent_universe(self):
        existing_universe = "t590"
        Morty.objects.create(universe=existing_universe, is_alive=True)
        data = {
            "universe": existing_universe
        }
        response = self.client.post(reverse('morties-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_morty_paired_with_already_paired_rick(self):
        rick = Rick.objects.create(universe="s360")
        Morty.objects.create(universe="t380", is_alive=True, paired_rick=rick)
        data = {
            "universe": "s490",
            "paired_rick": rick.id
        }
        response = self.client.post(reverse('morties-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_morty_no_data(self):
        data = None
        response = self.client.post(reverse('morties-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_one_morty_missing_universe_data(self):
        data = {
            "universe": ""
        }
        response = self.client.post(reverse('morties-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_morty(self):
        modified_universe = "t390"
        new_morty = Morty.objects.create(universe="t380", is_alive=True)
        self.assertFalse(Morty.objects.filter(universe=modified_universe).exists())
        data = {
            "universe": modified_universe
        }
        response = self.client.put(reverse('morties-detail', args=(new_morty.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Morty.objects.filter(universe=modified_universe).exists())

    def test_update_one_morty_paired_with_already_paired_rick(self):
        already_paired_rick = Rick.objects.create(universe="s360")
        rick2 = Rick.objects.create(universe="t480")
        Morty.objects.create(universe="t380", is_alive=True, paired_rick=already_paired_rick)
        new_morty = Morty.objects.create(universe="t490", is_alive=False, paired_rick=rick2)
        data = {
            "universe": new_morty.universe,
            "is_alive": new_morty.is_alive,
            "paired_rick": already_paired_rick.id
        }
        response = self.client.put(reverse('morties-detail', args=(new_morty.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_morty_no_data(self):
        new_morty = Morty.objects.create(universe="t380", is_alive=True)
        data = None
        response = self.client.put(reverse('morties-detail', args=(new_morty.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_morty_missing_universe_field_data(self):
        new_morty = Morty.objects.create(universe="t380", is_alive=True)
        data = {
            "universe": ""
        }
        response = self.client.put(reverse('morties-detail', args=(new_morty.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_one_morty_non_existent_id(self):
        data = {
            "universe": "t390"
        }
        response = self.client.put(reverse('morties-detail', args=(5,)), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_one_morty(self):
        checked_universe = "t590"
        new_morty = Morty.objects.create(universe=checked_universe, is_alive=True)
        self.assertTrue(Morty.objects.filter(universe=checked_universe).exists())

        response = self.client.delete(reverse('morties-detail', args=(new_morty.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Morty.objects.filter(universe="t590").exists())

    def test_delete_one_morty_non_existent_id(self):
        response = self.client.delete(reverse('morties-detail', args=(5,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
