from datetime import timedelta

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db.models import Count, Sum, Value, F,Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from app.models import Tag, Profile


def popular_tags():
    three_months_ago = timezone.now() - timedelta(days=90)
    return Tag.objects.annotate(
        q_count=Count('question', filter=Q(question__created_at__gte=three_months_ago))
    ).filter(q_count__gt=0).order_by('-q_count')[:10]


def popular_profiles():
    week_ago = timezone.now() - timedelta(days=7)

    question_ratings = Profile.objects.annotate(
        question_score=Coalesce(
            Sum('question__votes__value', filter=Q(question__created_at__gte=week_ago)),
            Value(0)
        )
    )

    answer_ratings = question_ratings.annotate(
        answer_score=Coalesce(
            Sum('answer__votes__value', filter=Q(answer__created_at__gte=week_ago)),
            Value(0)
        )
    )

    return answer_ratings.annotate(
        total_score=F('question_score') + F('answer_score')
    ).order_by('-total_score')[:10]


class Command(BaseCommand):
    def handle(self, *args, **options):
        p_tags = popular_tags()
        cache.set('popular_tags', p_tags, 360)
        p_profiles = popular_profiles()
        cache.set('popular_profiles', p_profiles, 360)
        print("кэш обновлен")
        print(cache.get('popular_profiles'), cache.get('popular_tags'))