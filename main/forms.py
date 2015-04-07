from django import forms
from django.contrib.auth import authenticate
from django.forms.utils import ErrorList
from models import ApplicationUser, Playlist

from django.core import validators
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)


class SignInModelForm(forms.ModelForm):
    class Meta:
        model = ApplicationUser
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(),
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super(SignInModelForm, self).__init__(*args, **kwargs)
        self.user_cache = None
        self.helper = FormHelper(self)
        self.helper.form_action = '/signin/'
        self.helper.layout = Layout('username', 'password', Submit('sign_in', 'Sign In'),)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = ApplicationUser.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            self._errors['username'] = ErrorList(["incorrect name or password", ])
        else:
            self.user_cache = authenticate(username=username, password=password)
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class SignUpForm(forms.ModelForm):
    class Meta:
        model = ApplicationUser
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.user_cache = None
        self.helper = FormHelper(self)
        self.helper.form_action = '/signup/'
        self.helper.layout = Layout(
            'username',
            'email',
            'password',
            'password_confirmation',
            Submit('sign_up', 'Sign Up'),
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if ApplicationUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if validators.validate_email(email):
            raise forms.ValidationError('Email is not valid')
        if ApplicationUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already in use')
        return email


    def clean(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if not password or not password_confirmation or password != password_confirmation:
            self._errors['username'] = ErrorList([''])
            self._errors['password'] = ErrorList(['Bad passwords', ])
        return self.cleaned_data

    def save(self, commit=True):
        user = ApplicationUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.save()
        return authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])


class AudioUploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(AudioUploadForm, self).__init__(*args, **kwargs)
        self.user_cache = None
        self.helper = FormHelper(self)
        self.helper.form_action = '/file/upload/'
        self.helper.layout = Layout(
            'file',
            Submit('upload', 'upload'),
        )


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(CreatePlaylistForm, self).__init__(*args, **kwargs)
        self.user_cache = None
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('name'),
            'description',
            Submit('Create', 'create'),
        )

    def save(self, commit=True, user=None):
        playlist = super(CreatePlaylistForm, self).save(commit)
        if user:
            playlist.user = user
            playlist.save()
        return playlist