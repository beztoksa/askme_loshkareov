from multiprocessing.reduction import recv_handle

from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from django.contrib.auth.models import User
import random

from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

"""
Пользователи > 10 000.
Вопросы > 100 000.
Ответы > 1 000 000.
Тэги > 10 000.
Оценки пользователей > 2 000 000.

пользователей — равное ratio;
вопросов — ratio * 10;
ответы — ratio * 100;
тэгов - ratio;
оценок пользователей - ratio * 200;

"""

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        Answer.objects.all().delete()
        User.objects.all().delete()
        Tag.objects.all().delete()
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        Profile.objects.all().delete()
        ratio = options["ratio"]
        fake = Faker('en_Us', use_weighting=False)
        db_batch_limit = 1000
        users_records = []
        user_names = [fake.unique.user_name() for _ in range(ratio)]
        for i in range(ratio):
            user = User(username=user_names[i], email=fake.email(), password=fake.password())
            users_records.append(user)
            if i == ratio-1 or i//db_batch_limit!=0:
                User.objects.bulk_create(users_records)
                users_records.clear()
        profiles_records = []
        user_ids = User.objects.values_list('id', flat=True)
        for i in range(ratio):
            profile = Profile(user_id=user_ids[i],rating=fake.random_int(0,ratio),avatar=fake.image_url())
            profiles_records.append(profile)
            if i == ratio-1 or i//db_batch_limit!=0:
                Profile.objects.bulk_create(profiles_records)
                profiles_records.clear()

        tags_records = []
        tag1 = [fake.unique.word() for _ in range(200)]
        fake.unique.clear()
        tag2 = [fake.unique.word() for _ in range(200)]
        tags_names = [tag1[i] + tag2[k] for i in range(200) for k in range(200)]
        for i in range(ratio):
            tag = Tag(name=tags_names[i])
            tags_records.append(tag)
            if i == ratio-1 or i//db_batch_limit!=0:
                Tag.objects.bulk_create(tags_records)
                tags_records.clear()

        question_records = []
        count_q =ratio*10
        profiles_ids = list(Profile.objects.values_list('id', flat=True))
        for i in range(count_q):
            question = Question(title=fake.sentence(), content=fake.text(),
                                profile_id=random.choice(profiles_ids), rating=fake.random_int(0, count_q))
            question_records.append(question)
            if i == count_q-1 or i//db_batch_limit!=0:
                Question.objects.bulk_create(question_records)
                question_records.clear()

        answers_records = []
        count_a =ratio*100
        #profiles_ids = list(Profile.objects.values_list('id', flat=True))
        question_ids = list(Question.objects.values_list('id', flat=True))
        for i in range(count_a):
            answer = Answer(content=fake.text(),profile_id=random.choice(profiles_ids),rating=fake.random_int(0,count_a), question_id = random.choice(question_ids))
            answers_records.append(answer)
            if i == count_a-1 or i//db_batch_limit!=0:
                Answer.objects.bulk_create(answers_records)
                answers_records.clear()

        question_ids = list(Question.objects.values_list('id', flat=True))
        tags_question_records = []
        amount =0
        tags_ids = list(Tag.objects.values_list('id', flat=True))
        random.shuffle(tags_ids)
        rand_num_tags = 2  # random.randint(0, len(tags)-1)
        tags_question_ids = tags_ids[0:rand_num_tags]
        for question_id in question_ids :


            for tag_id in tags_question_ids:
                question_tag = Question.tags.through(tag_id=tag_id, question_id=question_id)
                tags_question_records.append(question_tag)
                amount +=1

                if  amount//db_batch_limit!=0:
                    Question.tags.through.objects.bulk_create(tags_question_records)
                    amount =0
                    tags_question_records.clear()
        if tags_question_records:
            Question.tags.through.objects.bulk_create(tags_question_records)

        if ratio>=20:
            count_q = ratio*10
            count_like_question = ratio * 100
            count_profiles = count_like_question // count_q
            profiles_ids = list(Profile.objects.values_list('id', flat=True))
            question_ids = list(Question.objects.values_list('id', flat=True))
            like_question_records = []
            amount = 0
            count_question_profiles = count_profiles
            question_profile_ids = profiles_ids[:count_question_profiles]
            for question_id in question_ids:
               # count_question_profiles =random.randint(count_profiles,count_profiles+10)
                for profile_id in question_profile_ids:
                    question_like = QuestionLike(question_id=question_id,profile_id=profile_id)
                    like_question_records.append(question_like)
                    amount +=1
                    if amount==count_like_question or amount//db_batch_limit!=0:
                        QuestionLike.objects.bulk_create(like_question_records)
                        like_question_records.clear()

            count_a = ratio*100
            count_like_answer = ratio * 100
            count_profiles = count_like_answer // count_a
            profiles_ids = list(Profile.objects.values_list('id', flat=True))
            answer_ids = list(Answer.objects.values_list('id', flat=True))
            like_answer_records = []
            amount = 0
            count_answer_profiles = count_profiles
            answer_profile_ids = profiles_ids[:count_answer_profiles]
            for answer_id in answer_ids:
                #count_answer_profiles =random.randint(count_profiles,count_profiles+10)
                for profile_id in answer_profile_ids:
                    answer_like = AnswerLike(answer_id=answer_id,profile_id=profile_id)
                    like_answer_records.append(answer_like)
                    amount +=1
                    if amount==count_like_answer or amount//db_batch_limit!=0:
                        AnswerLike.objects.bulk_create(like_answer_records)
                        like_answer_records.clear()


        self.stdout.write(
            self.style.SUCCESS(f'ratio: {ratio}')
        )
