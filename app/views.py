from copy import deepcopy

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from app.models import Question, Tag



def paginate(objects_list, request, per_page=10):
    try:
        page_number = int(request.GET.get('page', 1))
    except ValueError:
        page_number = 1
    paginator = Paginator(objects_list, 5)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(1)
    return page


# Create your views here.
def index(request):

    page = paginate(Question.objects.new(), request, per_page=5)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page})


def hot(request):
    page = paginate(Question.objects.hot(), request, per_page=5)
    return render(request, 'hot.html', context={'hot_questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    page = paginate(question.answers(), request, per_page=5)
    return render(request, 'single_question.html', context={'question': question,'answers': page.object_list, 'page_obj': page})

def tag(request, tag_name):
    try:
        tag = Tag.objects.get(name=tag_name)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    page = paginate(tag.questions_of_tag(), request, per_page=5)
    return render(request, 'tag.html' , context={'tag_questions': page.object_list, 'page_obj':page,'tag':tag})
def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
def ask(request):
    return render(request, 'ask.html')