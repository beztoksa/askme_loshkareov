from datetime import timedelta
from enum import unique
from urllib import request

from bs4.diagnose import profile
from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Count, Sum, Value, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from parso.python.tree import Class

from askme_loshkareov.settings import MEDIA_ROOT


# Create your models here.
class QuestionManager(models.Manager):
    def hot(self):
        return Question.objects.annotate(score=Coalesce(Sum('votes__value'), Value(0))).order_by('-score')
    def new(self):
        return Question.objects.order_by('-created_at')
class TagManager(models.Manager):
    def popular_tags(self):
        three_months_ago = timezone.now() - timedelta(days=90)
        return self.annotate(
            q_count=Count('question', filter=models.Q(question__created_at__gte=three_months_ago))
        ).filter(q_count__gt=0).order_by('-q_count')[:10]
class ProfileManager(models.Manager):
    def popular_profiles(self):
        week_ago = timezone.now() - timedelta(days=7)

        question_ratings = Profile.objects.annotate(
            question_score=Coalesce(
                Sum('question__votes__value', filter=models.Q(question__created_at__gte=week_ago)),
                Value(0)
            )
        )

        answer_ratings = question_ratings.annotate(
            answer_score=Coalesce(
                Sum('answer__votes__value', filter=models.Q(answer__created_at__gte=week_ago)),
                Value(0)
            )
        )

        return answer_ratings.annotate(
            total_score=F('question_score') + F('answer_score')
        ).order_by('-total_score')[:10]

class Profile(models.Model):
    avatar = models.ImageField(upload_to='uploads/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProfileManager()

class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(default='')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
    def answers(self):
        return self.answer_set.all().order_by('-created_at')
    def rating(self):
        return QuestionLike.objects.filter(question=self).aggregate(models.Sum('value'))['value__sum'] or 0
    def get_user_vote(self, profile):
        if not profile.user.is_authenticated:
            return 0
        vote = QuestionLike.objects.filter(profile=profile, question=self).first()
        return vote.value if vote else 0
    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            GinIndex(
                SearchVector('title', 'content', config='russian'),
                name='question_search_idx',
            ),        ]


class QuestionLike(models.Model):
    QUESTION_VOTE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=QUESTION_VOTE_CHOICES, default=1)
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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def rating(self):
        return AnswerLike.objects.filter(answer=self).aggregate(models.Sum('value'))['value__sum'] or 0
    def get_user_vote(self, profile):
        if not profile.user.is_authenticated:
            return 0
        vote = AnswerLike.objects.filter(profile=profile, answer=self).first()
        return vote.value if vote else 0


class AnswerLike(models.Model):
    ANSWER_VOTE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=ANSWER_VOTE_CHOICES, default=1)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'answer'], name='unique_answer'),
            #models.UniqueConstraint('profile', 'answer', name='unique_profile'), тоже самое что индексы
        ]
class Tag(models.Model):
    objects = TagManager()
    name = models.CharField(max_length=255,unique=True)
    def questions_of_tag(self):
        return self.question_set.all().order_by('-created_at')

    def __str__(self):
        return self.name
