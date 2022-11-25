from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Genre,Artist,Album,Magazine,Review,Track
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.db.models import Avg, IntegerField
from django.db.models.functions import Round, Cast
from django.db import IntegrityError
from django.core.paginator import Paginator
import random

import json

class IndexView(generic.ListView):
    model: Album
    template_name = 'critics/index.html'
    context_object_name = 'latest_album_list'
    paginate_by = 9

    def get_queryset(self):
        latest = Album.objects.latest('id')
        album_list = Album.objects.order_by('-id').exclude(id=latest.id)

        query = self.request.GET.get('q')
        if query:
            album_list = Album.objects.filter(name__icontains=query)
        else:
            album_list = Album.objects.order_by('-id').exclude(id=latest.id)
        return album_list

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['latest'] = Album.objects.latest('id')
        return context

class AlbumDetailView(generic.DetailView):
    model = Album
    template_name = 'critics/album.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        context['tracklist'] = sorted(Track.objects.filter(parent_album=self.get_object()).order_by('place_in_tracklist'), key=lambda m: m.rating, reverse=True)
        return context

class ArtistIndexView(generic.ListView):
    model = Artist
    template_name = 'critics/artist_index.html'
    context_object_name = 'latest_artist_list'
    paginate_by = 9

    def get_queryset(self):
        artist_list = Artist.objects.order_by('name')

        query = self.request.GET.get('q')
        if query:
            artist_list = Artist.objects.filter(name__icontains=query)
        else:
            artist_list = Artist.objects.order_by('name')
        return artist_list

    def get_context_data(self, **kwargs):
        context = super(ArtistIndexView, self).get_context_data(**kwargs)
        items = list(Artist.objects.all())
        context['random_artist'] = random.choice(items)
        return context

class ArtistDetailView(generic.DetailView):
    model = Artist
    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['best_tracks'] = sorted(Track.objects.filter(parent_album__artist=self.get_object()), key=lambda m: m.rating, reverse=True)[:5]
        context['worst_tracks'] = sorted(Track.objects.filter(parent_album__artist=self.get_object()), key=lambda m: m.rating)[:5]
        context['best_reviews'] = Review.objects.filter(artist=self.get_object()).order_by('-rating')[:5]
        context['worst_reviews'] = Review.objects.filter(artist=self.get_object()).order_by('rating')[:5]
        return context
    template_name = 'critics/artist.html'

#def magazine_index(request):
#    latest_magazine_list = Magazine.objects.order_by('name')[:100]
#    context = {'latest_magazine_list': latest_magazine_list}
#    return render(request, 'critics/magazine_index.html', context)

class MagazineIndexView(generic.ListView):
    model = Magazine
    template_name = 'critics/magazine_index.html'
    context_object_name = 'latest_magazine_list'
    paginate_by = 9

    def get_queryset(self):
        magazine_list = Magazine.objects.order_by('name')

        query = self.request.GET.get('q')
        if query:
            magazine_list = Magazine.objects.filter(name__icontains=query)
        else:
            magazine_list = Magazine.objects.order_by('name')
        return magazine_list

    def get_context_data(self, **kwargs):
        context = super(MagazineIndexView, self).get_context_data(**kwargs)
        items = list(Album.objects.all())
        context['random_album'] = random.choice(items)
        return context
    
class MagazineDetailView(generic.DetailView):
    model = Magazine
    template_name = 'critics/magazine.html'

    def get_context_data(self, **kwargs):
        context = super(MagazineDetailView, self).get_context_data(**kwargs)
        context['best_artists'] = Artist.objects.filter(reviews__magazine=self.get_object()).order_by('reviews')[:5]
        context['worst_artists'] = Artist.objects.filter(reviews__magazine=self.get_object()).order_by('-reviews')[:5]
        return context
