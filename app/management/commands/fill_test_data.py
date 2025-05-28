from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from datetime import timedelta
import random

from app.models import Profile, Question, Answer, QuestionLike, AnswerLike, Tag

fake = Faker()

class Command(BaseCommand):
    help = 'Генерация тестовых данных'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание пользователей и профилей...')
        profiles = []
        for i in range(15):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            profile = Profile.objects.create(
                user=user,
                nickname=fake.first_name(),
                rating=random.randint(0, 100)
            )
            profiles.append(profile)

        self.stdout.write('Создание тегов...')
        tags = []
        for i in range(10):
            tag = Tag.objects.create(name=fake.word())
            tags.append(tag)

        self.stdout.write('Создание вопросов...')
        questions = []
        for _ in range(50):
            profile = random.choice(profiles)
            q_date = timezone.now() - timedelta(days=random.randint(0, 120))  # от сегодня до 4 месяцев назад
            print(q_date)
            q = Question.objects.create(
                profile=profile,
                title=fake.sentence(),
                content=fake.paragraph(),
                created_at=q_date
            )
            q.tags.set(random.sample(tags, k=random.randint(1, 3)))
            questions.append(q)

        self.stdout.write('Создание ответов...')
        answers = []
        for _ in range(100):
            profile = random.choice(profiles)
            question = random.choice(questions)
            a_date = timezone.now() - timedelta(days=random.randint(0, 7))  # за последнюю неделю
            a = Answer.objects.create(
                profile=profile,
                content=fake.text(),
                question=question,
                created_at=a_date
            )
            answers.append(a)

        self.stdout.write('Создание лайков к вопросам...')
        for question in questions:
            voters = random.sample(profiles, k=random.randint(0, 5))
            for voter in voters:
                QuestionLike.objects.get_or_create(
                    question=question,
                    profile=voter,
                    defaults={'value': random.choice([1, 1, 1, -1])}
                )

        self.stdout.write('Создание лайков к ответам...')
        for answer in answers:
            voters = random.sample(profiles, k=random.randint(0, 5))
            for voter in voters:
                AnswerLike.objects.get_or_create(
                    answer=answer,
                    profile=voter,
                    defaults={'value': random.choice([1, 1, 1, -1])}
                )

        self.stdout.write(self.style.SUCCESS('База успешно заполнена тестовыми данными.'))
