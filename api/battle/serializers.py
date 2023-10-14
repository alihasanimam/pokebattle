from rest_framework import serializers
from user.models import Battle


class BattleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Battle
        fields = ['id', 'url', 'challenger', 'defender', 'winner', 'user', 'user_id', 'data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'url', 'user', 'user_id', 'created_at', 'updated_at']
        extra_kwargs = {
            "winner": {"required": False, "allow_null": True}
        }


class PokemonSerializer(serializers.Serializer):
    abilities = serializers.ListField()
    forms = serializers.ListField()
    game_indices = serializers.ListField()
    height = serializers.IntegerField()
    held_items = serializers.ListField()
    id = serializers.IntegerField()
    is_default = serializers.BooleanField()
    location_area_encounters = serializers.CharField()
    moves = serializers.ListField()
    name = serializers.CharField()
    order = serializers.IntegerField()
    past_types = serializers.ListField()
    species = serializers.DictField()
    sprites = serializers.DictField()
    stats = serializers.ListField()
    types = serializers.ListField()
    weight = serializers.IntegerField()

