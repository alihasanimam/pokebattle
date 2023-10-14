from django.urls import reverse
from user.models import User, Battle
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.cache import cache

class BattleTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('test', 'test@example.com', 'testtest')
        self.battle = Battle.objects.create(challenger="ditto", defender="gengar", winner="gengar", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_can_search_pokemon(self):
        url = reverse('battle-pokemon')
        response = self.client.get(url, {'name': 'ditto'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), 'ditto')

    def test_search_pokemon_is_cached(self):
        url = reverse('battle-pokemon')
        response = self.client.get(url, {'name': 'ditto'})
        cached_pokemon = cache.get("pokemon_ditto")
        self.assertNotEqual(cached_pokemon, None)
    
    def test_search_pokemon_not_found(self):
        url = reverse('battle-pokemon')
        response = self.client.get(url, {'name': 'notapokemon'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_list_battles(self):
        url = reverse('battle-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_filter_battles(self):
        url = reverse('battle-list')
        response = self.client.get(url, {'search': 'ditto'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

        response = self.client.get(url, {'search': 'lucario'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)

    def test_can_create_battle(self):
        url = reverse('battle-list')
        response = self.client.post(url, {'challenger': 'ditto', 'defender': 'lucario'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('winner'), 'lucario')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)
    
    def test_can_delete_battle(self):
        url = reverse('battle-list')
        response = self.client.delete('{}{}/'.format(url, self.battle.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        count = Battle.objects.count()
        self.assertEqual(count, 0)