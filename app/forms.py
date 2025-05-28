from django import forms
from django.contrib.auth import authenticate
from django.template.context_processors import request

from app.models import User, Profile, Question, Tag, Answer


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    # def clean_username(self):
    #     if len(self.cleaned_data.get("username")) > 10:
    #         raise forms.ValidationError('username', "Username must be at least 3 characters long.")
    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     if username[0].lower() != 'a':
    #         self.add_error('username', 'Username must start with "a"')
    #     return cleaned_da


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'nickname']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    field_order = ['username', 'email', 'nickname', 'password', 'confirm_password', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', 'password does not match')
        return cleaned_data

    def clean_username(self):
        cleaned_data = self.cleaned_data.get('username')
        if User.objects.filter(username=cleaned_data).exists():
            self.add_error('username', 'username already used')
        return cleaned_data

    def clean_email(self):
        cleaned_data = self.cleaned_data.get('email')
        if User.objects.filter(email=cleaned_data).exists():
            self.add_error('email', 'email already used')
        return cleaned_data

    def save(self):
        profile = super().save(commit=False)
        user = User.objects.create_user(username=self.cleaned_data.get('username'), email=self.cleaned_data.get('email'),
                                   password=self.cleaned_data.get('password'))
        profile.user = user
        profile.user.save()
        profile.save()
        return profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'nickname']

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    field_order = ['username', 'email', 'nickname', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email
        self.fields['nickname'].initial = self.instance.nickname
        self.fields['avatar'].initial = self.instance.avatar

    def clean_username(self):
        cleaned_data = self.cleaned_data.get('username')
        if User.objects.filter(username=cleaned_data).exists() and self.instance.user.username != cleaned_data:
            self.add_error('username', 'username already used')
        return cleaned_data

    def clean_email(self):
        cleaned_data = self.cleaned_data.get('email')
        if User.objects.filter(email=cleaned_data).exists() and self.instance.user.email != cleaned_data:
            self.add_error('email', 'email already used')
        return cleaned_data

    def save(self):
        profile = super().save(commit=False)
        profile.user.username = self.cleaned_data.get('username')
        profile.user.email = self.cleaned_data.get('email')
        profile.user.save()
        profile.save()
        return profile


class QuestionCreateForm(forms.ModelForm):
    tag_names = forms.CharField(label='Tags', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
                                help_text='Enter comma separated tag names')

    class Meta:
        model = Question
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self):
        question = super().save(commit=False)
        question.profile = self.request.user.profile
        question.save()
        for tag_name in self.cleaned_data['tag_names'].strip().split(','):
            if tag_name:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
        question.save()
        return question


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.question_id = kwargs.pop('question_id', None)
        super().__init__(*args, **kwargs)

    def save(self):
        answer = super().save(commit=False)
        answer.profile = self.request.user.profile
        answer.question_id = self.question_id
        answer.save()
        return answer

