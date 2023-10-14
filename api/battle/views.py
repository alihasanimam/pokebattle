import requests
from django.core.cache import cache
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
from api.user.permissions import IsOwnerOfObject
from user.models import Battle
from api.battle.serializers import BattleSerializer, PokemonSerializer


class BattleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows searching, performing and managing battles.
    """
    # queryset = Battle.objects.filter().order_by('-created_at')
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfObject]
    filter_backends = [filters.SearchFilter]
    search_fields = ['challenger', 'defender']

    def get_queryset(self):
        """
        This view should return a list of all the battles
        for the currently authenticated user.
        """
        return Battle.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        This view takes two pokemon names and perform a battle to decide winner.
        """
        challenger = self.request.data.get('challenger', '').lower()
        defender = self.request.data.get('defender', '').lower()
        winner = self.perform_battle(challenger, defender)
        serializer.save(user=self.request.user, winner=winner)

    @action(methods=["get"], detail=False, url_path="pokemon", url_name="pokemon")
    def pokemon(self, request, *args, **kwargs):
        """
        This view takes a pokemon name and fetch result from https://pokeapi.co.
        Subsequent requests are cached to avoid excessive API calls.
        """
        name = request.query_params.get("name", '').lower()
        response = self.get_pokemon(name)
        serializer = PokemonSerializer(response)
        return Response(serializer.data)
    
    def get_pokemon(self, name):
        """
        Takes a pokemon name as input and return result by fatching data from https://pokeapi.co.
        The fetched data are cached and subsequent response are served from the cache.
        """
        cached_response = cache.get("pokemon_{}".format(name))
        if cached_response:
            return cached_response
        
        response = requests.get('https://pokeapi.co/api/v2/pokemon/{}'.format(name))
        if response.status_code == status.HTTP_200_OK:
            cache.set("pokemon_{}".format(name), response.json())
            return response.json()
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            raise NotFound(detail="Error 404, pokemon not found!", code=404)
        else:
            raise APIException(detail="Server error / Network issue!", code=500)


    def perform_battle(self, challenger, defender):
        """
        Perform a battle between two pokemons. The winner is decided by 
        combining winner of difference in all the stats.
        """
        challenger_pokemon = self.get_pokemon(challenger)
        defender_pokemon = self.get_pokemon(defender)
        challenger_point = 0
        defender_point = 0
        # hp
        if challenger_pokemon["stats"][0].get("base_stat", 0) > defender_pokemon["stats"][0].get("base_stat", 0):
            challenger_point += 1
        else:
            defender_point += 1
        
        # attack & defense
        if challenger_pokemon["stats"][1].get("base_stat", 0) + challenger_pokemon["stats"][2].get("base_stat", 0) > defender_pokemon["stats"][1].get("base_stat", 0) + defender_pokemon["stats"][2].get("base_stat", 0):
            challenger_point += 1
        else:
            defender_point += 1

        # special attack & special defense
        if challenger_pokemon["stats"][3].get("base_stat", 0) + challenger_pokemon["stats"][4].get("base_stat", 0) > defender_pokemon["stats"][3].get("base_stat", 0) + defender_pokemon["stats"][4].get("base_stat", 0):
            challenger_point += 1
        else:
            defender_point += 1

        # speed
        if challenger_pokemon["stats"][5].get("base_stat", 0) > defender_pokemon["stats"][5].get("base_stat", 0):
            challenger_point += 1
        else:
            defender_point += 1
        
        # Return winner
        if challenger_point > defender_point:
            return challenger
        return defender
