from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Word(models.Model):
    text = models.CharField(max_length=100)
    meaning = models.TextField()

    def __str__(self):
        return self.text

class Games(models.Model):
    title = models.CharField(max_length=255)
    img = models.CharField(max_length=255)  # Store image URL or path
    rating = models.FloatField()
    color = models.CharField(max_length=50)
    aosDelay = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# Model to store adverb images, options, and correct answers
class AdverbQuestion(models.Model):
    image = models.URLField()
    correct_adverb = models.CharField(max_length=100)
    options = models.JSONField()  # Store multiple choices in JSON format

    def __str__(self):
        return f"Adverb Question: {self.correct_adverb}"
