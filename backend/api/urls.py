from django.urls import path
from .views import add_word, word_list  # Import from the same app
from api.views import adverblist   # Correct import from 'api.views'
from api import views

urlpatterns = [
    path('addwords/', add_word, name='add-word'),
    path('words/', word_list, name='word_list'),
    path('words/<int:word_id>/', views.delete_word, name='delete_word'),
    path('adverb-questions/', adverblist, name='adverb-questions'),
]
