# backend/api/views.py

from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
import random
from .models import Word, Games, AdverbQuestion  # Import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GamesSerializer, AdverbQuestionSerializer, WordSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect

class GamesList(APIView):
    def get(self, request):
        games = Games.objects.all()  # Fetch all games
        serializer = GamesSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WordList(APIView):
    def get(self, request):
        words = Word.objects.all()  # Fetch all words
        serializer = WordSerializer(words, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

class AdverbQuestionViewSet(viewsets.ModelViewSet):
    queryset = AdverbQuestion.objects.all()
    serializer_class = AdverbQuestionSerializer
    parser_classes = (MultiPartParser, FormParser)

def registerPage(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')  # Redirect after successful registration
    return render(request, 'accounts/register.html', {'form': form})

def random_word(request):
    try:
        words = Word.objects.values('text', 'meaning')
        if not words:
            return JsonResponse({'error': 'No words found in the database.'}, status=404)
        word = random.choice(words)
        return JsonResponse({'word': word['text'], 'meaning' : word ['meaning']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def game_list(request):
    try:
        games = Games.objects.all().values('title', 'img', 'rating', 'color', 'aosDelay')
        return JsonResponse({'games': list(games)}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def word_list(request):
    try:
        words = Word.objects.all().values('id','text', 'meaning')
        return JsonResponse({'word': list(words)}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def add_word(request):
    if request.method == 'POST':
        serializer = WordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Word added successfully!"}, status=201)
        else:
            
            return Response({"error": serializer.errors}, status=400)
        
def delete_word(request, word_id):
    try:
        word = Word.objects.get(id=word_id)
    except Word.DoesNotExist:
        return Response({"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND)
    
    word.delete()  
    return Response({"message": "Word deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_word(request, pk):
    try:
        word = Word.objects.get(pk=pk)
        serializer = WordSerializer(word)
        return Response(serializer.data)
    except Word.DoesNotExist:
        return Response({'error': 'Word not found'}, status=404)
    
@api_view(['GET'])
def adverblist(request):
    questions = AdverbQuestion.objects.all()
    serializer = AdverbQuestionSerializer(questions, many=True)
    return Response(serializer.data)    