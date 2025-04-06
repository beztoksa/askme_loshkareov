from enum import unique

from django.contrib.auth.models import User
from django.db import models
from parso.python.tree import Class


# Create your models here.
class QuestionManager(models.Manager):
    pass

class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(default='')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['rating']),
        ]

class QuestionLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'question'], name='unique_question'),
            #models.UniqueConstraint('profile', 'question', name='unique_profile'), тоже самое что индексы
        ]
    def __str__(self):
        return f'{self.profile.id} + {self.question.id}'
class Answer(models.Model):
    content = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    flag_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)


class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'answer'], name='unique_answer'),
            #models.UniqueConstraint('profile', 'answer', name='unique_profile'), тоже самое что индексы
        ]
class Tag(models.Model):
    name = models.CharField(max_length=255,unique=True)
    def __str__(self):
        return self.name
