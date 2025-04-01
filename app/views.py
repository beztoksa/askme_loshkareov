from copy import deepcopy

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for questions # {i}',
        'img_path': "/img/1.jpg",
        'tag': f'tag'
    } for i in range(30)
]
ANSWERS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for answers # {i}',
        'img_path': "/img/1.jpg"
    } for i in range(3)
]
isLogin = True


def paginate(objects_list, request, per_page=10):
    page_number = int(request.GET.get('page', 1))
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
    page = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page, 'isLogin': isLogin})


def hot(request):
    HOT_QUESTIONS = list(deepcopy(reversed(QUESTIONS)))
    page = paginate(HOT_QUESTIONS, request, per_page=5)
    return render(request, 'hot.html', context={'hot_questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    page = paginate(ANSWERS, request, per_page=5)
    return render(request, 'single_question.html', context={'question': QUESTIONS[question_id],'answers': page.object_list, 'page_obj': page})

def tag(request, tag):
    TAG_QUESTIONS = [question for question in QUESTIONS if question.get('tag') == tag]
    page = paginate(TAG_QUESTIONS, request, per_page=5)
    return render(request, 'tag.html' , context={'tag_questions': page.object_list, 'page_obj':page,'tag':tag})
def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def settings(request):
    return render(request, 'settings.html')
def ask(request):
    return render(request, 'ask.html')