from rest_framework import serializers
from .models import Games, AdverbQuestion, Word


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'text', 'meaning']

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'title', 'img', 'rating', 'color', 'aosDelay']

class AdverbQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = AdverbQuestion
        fields = ['id', 'image', 'correct_adverb', 'options']

    def get_options(self, obj):
        return obj.options if isinstance(obj.options, (dict, list)) else []  # Ensures valid JSON output
