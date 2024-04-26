from rest_framework.test import APITestCase
from .models import Rick
from django.urls import reverse
from rest_framework import status
from .serializers import RickSerializer


class RickTestCase(APITestCase):
    """
        Test for CRUD functionalities for the 'ricks' endpoint
    """
    def setUp(self):
        self.new_rick1 = Rick.objects.create(universe="t380", is_morty_alive=True)
        self.new_rick2 = Rick.objects.create(universe="t490", is_morty_alive=False)

    def test_get_all_ricks(self):
        response = self.client.get(reverse('ricks-list'))
        ricks = Rick.objects.all()
        serializer = RickSerializer(ricks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_one_rick(self):
        response = self.client.get(reverse('ricks-detail', args=(self.new_rick1.id,)))
        rick = Rick.objects.get(pk=self.new_rick1.id)
        serializer = RickSerializer(rick)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_one_rick(self):
        data = {
            "universe": "t380",
            "is_morty_alive": False
        }
        response = self.client.post(reverse('ricks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_one_rick(self):
        data = {
            "universe": "t390",
            "is_morty_alive": False
        }
        response = self.client.put(reverse('ricks-detail', args=(self.new_rick1.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rick = Rick.objects.get(pk=self.new_rick1.id)
        serializer = RickSerializer(rick)
        self.assertEqual(serializer.data.get('universe'), "t390")

    def test_delete_one_rick(self):
        response = self.client.delete(reverse('ricks-detail', args=(self.new_rick1.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Rick.DoesNotExist):
            Rick.objects.get(pk=self.new_rick1.id)
