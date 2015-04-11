import json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from forms import SignInModelForm, SignUpForm, AudioUploadForm, CreatePlaylistForm
from main.dropbox_api import Dropbox
from main.models import Audio, Playlist, Like
from dateutil.parser import parse
import urllib
from eyed3 import load
from eyed3 import core


def home(request):
    return render(request, 'home.html', {
        'user': request.user,
        'request': request,
        'audio_upload_form': AudioUploadForm(),
        'audio': request.user.audio.filter(deleted=False) if not request.user.is_anonymous() else []
    })

@login_required
def music(request):
    return render(request, 'music.html', {
        'user': request.user,
        'request': request,
        'audio': request.user.audio.filter(deleted=False)
    })

@login_required
def playlist(request):
    form = CreatePlaylistForm()
    if request.method == "POST":
        form = CreatePlaylistForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
    playlists = request.user.playlist.all()
    return render(request, 'playlists.html', {
        'request': request, 'form': form, 'playlists': playlists
    })


def playlist_popular(request):
    print Playlist.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')
    return render(request, 'playlist_popular.html', {
        'request': request,
        'playlists': Playlist.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')
    })

def new_track(request):
    pl = Audio.objects.filter(deleted=False).all().order_by('last_updated')
    print pl
    return render(request, 'new_track.html', {
        'request': request,
        'audio': pl
    })


@login_required
def playlist_info(request, id=None):
    try:
        pl = Playlist.objects.get(id=id)
    except Playlist.DoesNotExist:
        raise Http404
    return render(request, 'playlist.html', {
        'user': request.user,
        'request': request,
        'audio': pl.audio.filter(deleted=False),
        'playlist': pl,
        'liked': bool(Like.objects.filter(user=request.user, playlist=pl))
    })

@login_required
def playlist_edit(request, id=None):
    try:
        pl = Playlist.objects.get(id=id)
    except Playlist.DoesNotExist:
        raise Http404
    else:
        if request.user != pl.user:
            raise Http404
        if request.method == 'POST':
            ids = request.POST.getlist('ids', None)
            print ids
            if ids is not None:
                ids = [int(item) for item in ids]
                pl.audio.clear()
                tracks = Audio.objects.filter(id__in=ids)
                pl.audio.add(*tracks)
            return redirect(reverse('playlist_info', kwargs={'id': id}))
        return render(request, 'playlist_edit.html', {
            'request': request,
            'audio': request.user.audio.filter(deleted=False),
            'playlist': pl
        })


@login_required
@csrf_exempt
def playlist_like_ajax(request, id=None):
    try:
        pl = Playlist.objects.get(id=id)
    except Playlist.DoesNotExist:
        raise Http404
    else:
        like, created = Like.objects.get_or_create(user=request.user, playlist=pl)
        if not created:
            like.delete()
        return HttpResponse(json.dumps({'liked': created}), content_type="application/json")



@login_required
def playlist_delete(request, id=None):
    try:
        pl = Playlist.objects.get(id=id)
    except Playlist.DoesNotExist:
        raise Http404
    else:
        if request.user != pl.user:
            raise Http404
        pl.delete()
        return redirect('playlist')


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
            audiofile = load(file.temporary_file_path())
            Audio.objects.create(artist=audiofile.tag.artist,
                                 title=audiofile.tag.title,
                                 url=data['url'],
                                 expires=parse(data['expires']),
                                 owner=request.user,
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
    context = {
        "message": "ok"
    }
    if file:
        data = Dropbox().upload(file)
        audiofile = load(file.temporary_file_path())
        print dir(audiofile)
        print '/////////////////////'
        print dir(audiofile.tag)
        audio = Audio.objects.create(artist=audiofile.tag.artist,
                                     title=audiofile.tag.title,
                                     url=data['url'],
                                     expires=parse(data['expires']),
                                     owner=request.user,
                                     path=data['path'])
        request.user.audio.add(audio)
        context['name'] = audio.name
        context['url'] = audio.url
        context['id'] = audio.id
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@csrf_exempt
def file_delete_ajax(request):
    id = request.GET.get('id', None)
    if not id:
        raise Http404
    track = Audio.objects.filter(id=id).first()
    if track and track.owner != request.user:
        raise Http404
    track.deleted = True
    track.save()
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")
