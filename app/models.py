from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from parso.python.tree import Class


# Create your models here.
# Пока откладываю делать лайк
class QuestionManager(models.Manager):
    pass

class Profile(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Question(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField('Tag')
    like_count = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class QuestionLike(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)

class Answer(models.Model):
    content = models.TextField()
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    flag_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.PROTECT)

class AnswerLike(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
