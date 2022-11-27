from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Genre,Artist,Album,Magazine,Review,Track,ReviewTrack,List
from django.template import loader
from django.views import generic
from django.urls import reverse
from django.db.models import Avg, IntegerField
from django.db.models.functions import Round, Cast
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
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
        
        revs = Review.objects.filter(album=self.get_object())
        good = 0
        mixed = 0
        bad = 0
        total = len(revs)
        for x in revs:
            if x.rating > 69:
                good += 1
            elif x.rating < 50:
                bad += 1
            else:
                mixed += 1

        context['good'] = good
        context['mixed'] = mixed
        context['bad'] = bad
        context['total'] = total

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

        alb = Album.objects.filter(artist=self.get_object())
        epc = 0
        lpc = 0
        for x in alb:
            if x.tracks > 8:
                lpc += 1
            else:
                epc += 1

        context['epc'] = epc
        context['lpc'] = lpc

        revs = Review.objects.filter(artist=self.get_object())
        good = 0
        mixed = 0
        bad = 0
        total = len(revs)
        for x in revs:
            if x.rating > 69:
                good += 1
            elif x.rating < 50:
                bad += 1
            else:
                mixed += 1

        context['good'] = good
        context['mixed'] = mixed
        context['bad'] = bad
        context['total'] = total

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
        reviewed_albums = self.get_reviewed_albums()
        context['best_tracks'] = ReviewTrack.objects.filter(review__magazine=self.get_object()).order_by('-rating')[:15]
        context['worst_tracks'] = ReviewTrack.objects.filter(review__magazine=self.get_object()).order_by('rating')[:15]
        context['reviewed_albums'] = reviewed_albums
        context['page_obj'] = reviewed_albums

        revs = Review.objects.filter(magazine=self.get_object())
        good = 0
        mixed = 0
        bad = 0
        total = len(revs)
        for x in revs:
            if x.rating > 69:
                good += 1
            elif x.rating < 50:
                bad += 1
            else:
                mixed += 1

        context['good'] = good
        context['mixed'] = mixed
        context['bad'] = bad
        context['total'] = total

        return context

    def get_reviewed_albums(self):
        queryset = self.object.reviews.all() 
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        reviewed_albums = paginator.get_page(page)
        return reviewed_albums

class ListIndexView(generic.ListView):
    model = List
    template_name = 'critics/list_index.html'
    context_object_name = 'lists_list'

    def get_queryset(self):
        lists_list = List.objects.all().order_by('id')
        return lists_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alb_by_avg = sorted(Album.objects.all(), key=lambda m: m.rating, reverse=True)
        alb_by_app = sorted(Album.objects.all(), key=lambda m: m.approve_index, reverse=True)[:10]
        alb_by_dis = sorted(Album.objects.all(), key=lambda m: m.disapprove_index, reverse=True)[:10]
        art_by_avg = sorted(Artist.objects.all(), key=lambda m: m.avg, reverse=True)
        art_by_app = sorted(Artist.objects.all(), key=lambda m: m.approve_index, reverse=True)[:10]
        art_by_dis = sorted(Artist.objects.all(), key=lambda m: m.disapprove_index, reverse=True)[:10]
        mag_by_avg = sorted(Magazine.objects.all(), key=lambda m: m.avg, reverse=True)
        mag_by_app = sorted(Magazine.objects.all(), key=lambda m: m.approve_index, reverse=True)[:10]
        mag_by_dis = sorted(Magazine.objects.all(), key=lambda m: m.disapprove_index, reverse=True)[:10]
        tra_by_best = sorted(Track.objects.all(), key=lambda m: m.rating, reverse=True)[:10]
        tra_by_worst = sorted(Track.objects.all(), key=lambda m: m.rating, reverse=False)[:10]
        
        context['big_alb_by_avg'] = alb_by_avg[0]
        context['big_alb_by_app'] = alb_by_app[0]
        context['big_alb_by_dis'] = alb_by_dis[0]
        context['big_art_by_avg'] = art_by_avg[0]
        context['big_art_by_app'] = art_by_app[0]
        context['big_art_by_dis'] = art_by_dis[0]
        context['big_mag_by_avg'] = mag_by_avg[0]
        context['big_mag_by_app'] = mag_by_app[0]
        context['big_mag_by_dis'] = mag_by_dis[0]
        context['big_tra_by_best'] = tra_by_best[0]
        context['big_tra_by_worst'] = tra_by_worst[0]
        return context
    
class ListDetailView(generic.DetailView):
    model = List
    template_name = 'critics/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListDetailView, self).get_context_data(**kwargs)

        if self.object.id == 1:
            alb_by_avg = self.get_alb_by_avg()
            context['list_content'] = alb_by_avg
            items = list(alb_by_avg)
            context['page_obj'] = alb_by_avg
        elif self.object.id == 2:
            alb_by_app = self.get_alb_by_app()
            context['list_content'] = alb_by_app
            items = list(alb_by_app)
            context['page_obj'] = alb_by_app
        elif self.object.id == 3:
            alb_by_dis = self.get_alb_by_dis()
            context['list_content'] = alb_by_dis
            items = list(alb_by_dis)
            context['page_obj'] = alb_by_dis
        elif self.object.id == 4:
            tra_by_best = self.get_tra_by_best()
            context['list_content'] = tra_by_best
            items = list(tra_by_best)
            context['page_obj'] = tra_by_best
        elif self.object.id == 5:
            tra_by_worst = self.get_tra_by_worst()
            context['list_content'] = tra_by_worst
            items = list(tra_by_worst)
            context['page_obj'] = tra_by_worst
        elif self.object.id == 6:
            art_by_avg = self.get_art_by_avg()
            context['list_content'] = art_by_avg
            items = list(art_by_avg)
            context['page_obj'] = art_by_avg
        elif self.object.id == 7:
            art_by_app = self.get_art_by_app()
            context['list_content'] = art_by_app
            items = list(art_by_app)
            context['page_obj'] = art_by_app
        elif self.object.id == 8:
            art_by_dis = self.get_art_by_dis()
            context['list_content'] = art_by_dis
            items = list(art_by_dis)
            context['page_obj'] = art_by_dis
        elif self.object.id == 9:
            mag_by_avg = self.get_mag_by_avg()
            context['list_content'] = mag_by_avg
            items = list(mag_by_avg)
            context['page_obj'] = mag_by_avg
        elif self.object.id == 10:
            mag_by_app = self.get_mag_by_app()
            context['list_content'] = mag_by_app
            items = list(mag_by_app)
            context['page_obj'] = mag_by_app
        elif self.object.id == 11:
            mag_by_dis = self.get_mag_by_dis()
            context['list_content'] = mag_by_dis
            items = list(mag_by_dis)
            context['page_obj'] = mag_by_dis

        context['avg_lists'] = [1,4,5,6,9]
        context['app_lists'] = [2,7,10]
        context['random_album'] = random.choice(items)

        return context

    def get_alb_by_avg(self):
        queryset = sorted(Album.objects.all(), key=lambda m: m.rating, reverse=True) 
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        alb_by_avg = paginator.get_page(page)
        return alb_by_avg

    def get_alb_by_app(self):
        queryset = sorted(sorted(Album.objects.all(), key=lambda m: m.rating, reverse=True), key=lambda m: m.approve_index, reverse=True)[:30]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        alb_by_app = paginator.get_page(page)
        return alb_by_app

    def get_alb_by_dis(self):
        queryset = sorted(sorted(Album.objects.all(), key=lambda m: m.rating, reverse=False), key=lambda m: m.disapprove_index, reverse=True)[:10]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        alb_by_dis = paginator.get_page(page)
        return alb_by_dis

    def get_tra_by_best(self):
        queryset = sorted(sorted(Track.objects.all(), key=lambda m: m.rating, reverse=True), key=lambda m: m.rating, reverse=True)[:10]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        tra_by_best = paginator.get_page(page)
        return tra_by_best

    def get_tra_by_worst(self):
        queryset = sorted(sorted(Track.objects.all(), key=lambda m: m.rating, reverse=True), key=lambda m: m.rating, reverse=False)[:10]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        tra_by_worst = paginator.get_page(page)
        return tra_by_worst

    def get_art_by_avg(self):
        queryset = sorted(sorted(Artist.objects.all(), key=lambda m: m.avg, reverse=True), key=lambda m: m.avg, reverse=True)
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        art_by_avg = paginator.get_page(page)
        return art_by_avg

    def get_art_by_app(self):
        queryset = sorted(sorted(Artist.objects.all(), key=lambda m: m.avg, reverse=True), key=lambda m: m.approve_index, reverse=True)[:30]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        art_by_app = paginator.get_page(page)
        return art_by_app
    
    def get_art_by_dis(self):
        queryset = sorted(sorted(Artist.objects.all(), key=lambda m: m.avg, reverse=True), key=lambda m: m.disapprove_index, reverse=True)[:10]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        art_by_dis = paginator.get_page(page)
        return art_by_dis

    def get_mag_by_avg(self):
        queryset = sorted(sorted(Magazine.objects.all(), key=lambda m: m.avg, reverse=True), key=lambda m: m.avg, reverse=True)
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        mag_by_avg = paginator.get_page(page)
        return mag_by_avg

    def get_mag_by_app(self):
        queryset = sorted(sorted(Magazine.objects.all(), key=lambda m: m.avg, reverse=True), key=lambda m: m.approve_index, reverse=True)[:30]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        mag_by_app = paginator.get_page(page)
        return mag_by_app

    def get_mag_by_dis(self):
        queryset = sorted(sorted(Magazine.objects.all(), key=lambda m: m.avg, reverse=True), key=lambda m: m.disapprove_index, reverse=True)[:10]
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        mag_by_dis = paginator.get_page(page)
        return mag_by_dis
