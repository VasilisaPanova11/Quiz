from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text

User = get_user_model()

class QuizResult(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answers_count = models.IntegerField(default=0)