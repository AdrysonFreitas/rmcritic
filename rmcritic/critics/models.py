from django.db import models
from django.db.models import Avg, Count, IntegerField
from django.db.models.functions import Round, Cast

class Genre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    count_review = models.IntegerField(default=0)
    avg = models.IntegerField(default=0)

    @property
    def avg(self):
        return self.reviews.aggregate(avg_rating=Cast(Round(Avg('rating')), output_field=IntegerField()))['avg_rating']

    @property
    def count_review(self):
        return self.reviews.aggregate(count_review=Count('rating'))['count_review']

    def genre_list(self):
        return ', '.join([a.name for a in self.genre.all()])
    genre_list.short_description = "Genres"

    class Meta:
        ordering = ['name']

    def __str__(self):
        #return f'{self.name} {self.avg} {self.count_review}'
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=300)
    artist = models.ForeignKey(Artist,
        on_delete=models.CASCADE,
        related_name='albums',)
    tracks = models.IntegerField(default=0)
    genre = models.ManyToManyField(Genre)
    count_review = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    @property
    def rating(self):
        return self.reviews.aggregate(avg_rating=Cast(Round(Avg('rating')), output_field=IntegerField()))['avg_rating']

    @property
    def count_review(self):
        return self.reviews.aggregate(count_review=Count('rating'))['count_review']

    @property
    def tracks(self):
        return self.tracklist.aggregate(tracks=Count('id'))['tracks']

    def genre_list(self):
        return ', '.join([a.name for a in self.genre.all()])
    genre_list.short_description = "Genres"
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        #return f'{self.name} {self.rating} {self.count_review}'
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=200)
    featuring = models.CharField(max_length=200,null=True,blank=True)
    parent_album = models.ForeignKey(Album,
        on_delete=models.CASCADE,
        related_name='tracklist',)
    parent_artist = models.ForeignKey(Artist,
        on_delete=models.CASCADE,
        related_name='tracks',)
    rating = models.IntegerField(default=0)
    place_in_tracklist = models.IntegerField(default=0)

    @property
    def rating(self):
        return self.reviews.aggregate(avg_rating=Cast(Round(Avg('rating')), output_field=IntegerField()))['avg_rating']

    class Meta:
        ordering = ['place_in_tracklist']

    def __str__(self):
        return self.name

class Magazine(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=300)
    alt_name = models.CharField(max_length=200,null=True,blank=True)
    adm = models.CharField(max_length=200)
    count_review = models.IntegerField(default=0)
    avg = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    @property
    def avg(self):
        return self.reviews.aggregate(avg_rating=Cast(Round(Avg('rating')), output_field=IntegerField()))['avg_rating']
    
    @property
    def count_review(self):
        return self.reviews.aggregate(count_review=Count('rating'))['count_review']

    class Meta:
        ordering = ['name']

    def __str__(self):
        #return f'{self.name} {self.avg} {self.count_review}'
        return self.name

class Review(models.Model):
    magazine = models.ForeignKey(Magazine,
        on_delete=models.CASCADE,
        related_name='reviews',)
    album = models.ForeignKey(Album,
        on_delete=models.CASCADE,
        related_name='reviews',)
    artist = models.ForeignKey(Artist,
        on_delete=models.CASCADE,
        related_name='reviews',)
    rating = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return str(self.album)

class ReviewTrack(models.Model):
    track = models.ForeignKey(Track,
        on_delete=models.CASCADE,
        related_name='reviews',)
    review = models.ForeignKey(Review,
        on_delete=models.CASCADE,
        related_name='parent_review',)
    rating = models.IntegerField(default=0)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return str(self.track)
