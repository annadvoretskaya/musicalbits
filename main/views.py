import json
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.db.models import Count, Avg, Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from forms import SignInModelForm, SignUpForm, AudioUploadForm, CreatePlaylistForm
from main.dropbox_api import Dropbox
from main.models import Audio, Playlist, Like, AudioRating, AudioConnection, ApplicationUser
from dateutil.parser import parse
import urllib
from eyed3 import load
from eyed3 import core


def home(request):
    return render(request, 'home.html', {
        'user': request.user,
        'request': request,
        # 'audio_upload_form': AudioUploadForm(),
        'audio': request.user.audio.filter(deleted=False).annotate(rating=Avg('ratings__value')) if not request.user.is_anonymous() else []
    })

def search(request):
    track = None
    if request.method == 'POST':
        input = request.POST['search']
        print request.POST
        track = Audio.objects.filter(Q(title__icontains=input)|Q(artist__icontains=input)|Q(genre__icontains=input))
    return render(request, 'music.html', {
        'request': request,
        'audio': track
    })

@login_required
def music(request):
    return render(request, 'music.html', {
        'user': request.user,
        'request': request,
        'audio': request.user.audio.filter(deleted=False).annotate(rating=Avg('ratings__value'))
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
        'request': request,
        'form': form,
        'playlists': playlists
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


def users(request):
    return render(request, 'users.html', {
        'request': request,
        'users': ApplicationUser.objects.all()
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
        'audio': pl.audio.filter(deleted=False).annotate(rating=Avg('ratings__value')).order_by('audioconnection__number'),
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
                for track in tracks:
                    AudioConnection.objects.create(playlist=pl, audio=track)
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


@login_required
@csrf_exempt
def file_add_ajax(request):
    id = request.GET.get('id', None)
    if not id:
        raise Http404
    track = Audio.objects.filter(id=id).first()
    if track and track.owner == request.user:
        raise Http404
    request.user.audio.add(track)
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")


@login_required
@csrf_exempt
def rate_track(request):
    id = request.GET.get('id', None)
    value = request.GET.get('value', None)
    user = request.user
    audio = Audio.objects.filter(id=id).first()
    if not audio:
        raise Http404
    rating, _ = AudioRating.objects.get_or_create(user=user, audio=audio)
    rating.value = value
    rating.save()
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")


@login_required
@csrf_exempt
def playlist_sort(request):
    pl_id = request.GET.get('id', None)
    ids = request.GET.get('ids', None)
    ids = ids.split(',')
    if not pl_id or not ids:
        raise Http404
    for index, id in enumerate(ids):
        con = AudioConnection.objects.filter(playlist__id=pl_id, audio__id=id).first()
        con.number = index
        con.save()
    return HttpResponse(json.dumps({'message': 'ok'}), content_type="application/json")


@login_required
@csrf_exempt
def playlist_edit_ajax(request):
    pl_id = request.GET.get('id', None)
    name = request.GET.get('name', None)
    desc = request.GET.get('desc', None)
    if not pl_id:
        raise Http404
    pl = Playlist.objects.filter(id=pl_id).first()
    if not pl or pl.user != request.user:
        raise Http404
    if name:
        pl.name = name
    if desc:
        pl.description = desc
    pl.save()
    return HttpResponse(json.dumps({'message': 'ok', 'desc': pl.description_html}), content_type="application/json")


@login_required
@csrf_exempt
def track_edit_ajax(request):
    id = request.GET.get('id')
    if not id:
        raise Http404
    track = Audio.objects.filter(id=id).first()
    if not track:
        raise Http404
    artist = request.GET.get('artist')
    title = request.GET.get('title')
    genre = request.GET.get('genre')
    if artist:
        track.artist = artist
    if title:
        track.title = title
    if genre:
        track.genre = genre

    track.save()

    return HttpResponse(json.dumps({'message': 'ok', 'title': track.title, 'artist': track.artist, 'genre': track.genre}), content_type="application/json")
