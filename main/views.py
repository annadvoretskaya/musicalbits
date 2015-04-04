import json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from forms import SignInModelForm, SignUpForm, AudioUploadForm
from main.dropbox_api import Dropbox
from main.models import Audio
from dateutil.parser import parse
import urllib
from eyed3 import load
from eyed3 import core


def home(request):
    return render(request, 'home.html', {
        'user': request.user,
        'request': request,
        'audio_upload_form': AudioUploadForm(),
        'audio': request.user.audio.all() if not request.user.is_anonymous() else []
    })

@login_required
def music(request):
    return render(request, 'music.html', {
        'user': request.user,
        'request': request,
        'audio': request.user.audio.all()
    })


def signin(request):
    sign_in_form = SignInModelForm()
    if request.method == 'POST':
        sign_in_form = SignInModelForm(request.POST)
        if sign_in_form.is_valid():
            user = sign_in_form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'home.html', {
        'sign_in_form': sign_in_form,
        'sing_up_form': SignUpForm()
    })


def signup(request):
    sing_up_form = SignUpForm()
    if request.method == 'POST':
        sing_up_form = SignUpForm(request.POST)
        if sing_up_form.is_valid():
            user = sing_up_form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'home.html', {
        'sing_up_form': sing_up_form,
        'sign_in_form': SignInModelForm()
    })


@login_required
def file_upload(request):
    if request.method == 'POST':
        file = request.FILES['file']

        if file:
            data = Dropbox().upload(file)
            # filename, headers = urllib.urlretrieve(data['url'])
            # print type(file)
            audiofile = load(file.temporary_file_path())
            # print str(audiofile.tag.artist.encode('utf-8'))
            # print type(audiofile.tag.artist.encode('utf-8'))
            Audio.objects.create(artist=audiofile.tag.artist,
                                 title=audiofile.tag.title,
                                 url=data['url'],
                                 expires=parse(data['expires']),
                                 user=request.user,
                                 path=data['path'])

            return redirect('home')
    raise Http404


def logout_user(request):
    print 'HERE'
    logout(request)
    return redirect('home')


@login_required
@csrf_exempt
def file_upload_ajax(request):
    file = request.FILES['uploadfile']
    if file:
        data = Dropbox().upload(file)
        audiofile = load(file.temporary_file_path())
        Audio.objects.create(artist=audiofile.tag.artist,
                             title=audiofile.tag.title,
                             url=data['url'],
                             expires=parse(data['expires']),
                             user=request.user,
                             path=data['path'])
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")