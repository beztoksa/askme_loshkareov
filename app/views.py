from audioop import reverse
from copy import deepcopy, error
from lib2to3.fixes.fix_input import context
from traceback import print_tb

from bs4.diagnose import profile
from cent import Client, PublishRequest
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from app.forms import LoginForm, ProfileCreateForm, ProfileUpdateForm, QuestionCreateForm, AnswerCreateForm
from app.models import Question, Tag, User, Profile, QuestionLike, Answer, AnswerLike
def get_cent_client():
    api_url = f'http://centrifugo:8000/api'
    client = Client(api_url, settings.CENTRIFUGO_API_KEY)
    return client

def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(objects_list, 5)
    try:
        page = paginator.page(page_number)
    except (PageNotAnInteger,EmptyPage):
        page = paginator.page(1)
    return page

class PackQuestion:
    def __init__(self, question, profile):
        self.question = question
        self.vote = question.get_user_vote(profile)
class PackAnswer:
    def __init__(self, answer, profile):
        self.answer = answer
        self.vote = answer.get_user_vote(profile)
def packing(page, profile, pack_class=PackQuestion):
    itmes = page.object_list
    packs = []
    for obj in itmes:
        pack = pack_class(obj, profile)
        packs.append(pack)
    return packs

@login_required(login_url='login')
# Create your views here.
def index(request):
    page = paginate(Question.objects.new(), request, per_page=5)
    packs = packing(page, request.user.profile, PackQuestion)
    return render(request, 'index.html', context={'packs': packs, 'page_obj': page})


def hot(request):
    page = paginate(Question.objects.hot(), request, per_page=5)
    packs = packing(page, request.user.profile, PackQuestion)
    return render(request, 'hot.html', context={'packs': packs, 'page_obj': page})


def question(request, question_id):
    #
    ws_channel = f"question_{question_id}"
    try:
        question = Question.objects.get(id=question_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    page = paginate(question.answers(), request, per_page=5)
    #
    packs = packing(page, request.user.profile, PackAnswer)
    pack = PackQuestion(question, request.user.profile)
    disable = question.profile != request.user.profile
    #
    form = AnswerCreateForm(request=request, question_id=question_id)
    if request.method == 'POST':
        form = AnswerCreateForm(request.POST, request=request, question_id = question_id)
        if form.is_valid():
            answer = form.save()
            data = {
                "avatar_url": request.user.profile.avatar.url if request.user.profile.avatar else "",
                "id": answer.id,
                "content": answer.content,
                "disable": disable
            }
            client = get_cent_client()
            centrifugo_request = PublishRequest(channel=ws_channel, data=data)
            client.publish(centrifugo_request)
            return redirect(f'{request.path}?page=1')
    #
    return render(request, 'single_question.html',
                  context={'pack': pack,
                           'packsans': packs,
                           'page_obj': page,
                           'form': form,
                           'disable': disable,
                           'ws_channel': ws_channel,
                           })


def tag(request, tag_name):
    try:
        tag = Tag.objects.get(name=tag_name)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    page = paginate(tag.questions_of_tag(), request, per_page=5)
    packs = packing(page, request.user.profile, PackQuestion)
    return render(request, 'tag.html', context={'packs': packs, 'page_obj': page, 'tag': tag})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('edit_profile'))
            else:
                form.add_error(field=None, error="User not found")
    return render(request, 'login.html', {'form': form})

"""
стоит ли переделовать форму?
сделать две формы или воспользоваться наследованием ? 
"""
def signup(request):
    form = ProfileCreateForm()
    if request.method == 'POST':
        form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            auth.login(request, profile.user)
            return redirect(reverse('index'))
    return render(request, 'signup.html', {'form': form})


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('edit_profile'))
    return render(request, 'settings.html',{'form': form})

@login_required(login_url=reverse_lazy('login'))
def ask(request):
    form = QuestionCreateForm()
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST, request = request)
        if form.is_valid():
            question = form.save()
            return redirect('question', question.id)
    return render(request, 'ask.html', {'form': form})
@login_required(login_url=reverse_lazy('login'))
def QuestionRating(request, question_id):
    print(request.POST)
    value = int(request.POST.get('value',0))
    question = Question.objects.get(id=question_id)
    vote, is_created = QuestionLike.objects.get_or_create(question=question, profile=request.user.profile, value=value)
    if not is_created:
        vote.delete()
        user_vote = 0
    else:
        user_vote = value
    return JsonResponse({'question_rating': question.rating(), 'user_vote': user_vote})




@login_required(login_url=reverse_lazy('login'))
def AnswerRating(request, answer_id):
    print(request.POST)
    value = int(request.POST.get('value',0))
    answer = Answer.objects.get(id=answer_id)
    vote, is_created = AnswerLike.objects.get_or_create(answer=answer, profile=request.user.profile, value=value)
    if not is_created:
        vote.delete()
        user_vote = 0
    else:
        user_vote = value
    return JsonResponse({'answer_rating': answer.rating(), 'user_vote': user_vote})
@login_required(login_url=reverse_lazy('login'))
def correct(request,question_id, answer_id):
    answer = Answer.objects.get(id=answer_id)
    question = Question.objects.get(id=question_id)
    if question.profile == request.user.profile:
        answer.flag_correct = not answer.flag_correct
        answer.save()
    print(answer.flag_correct)
    return JsonResponse({'correct': answer.flag_correct})

