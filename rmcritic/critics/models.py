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
    count_albums = models.IntegerField(default=0)

    @property
    def avg(self):
        r = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        r = round(r)
        if r is None:
            r = 0
        return r

    @property
    def count_review(self):
        return self.reviews.aggregate(count_review=Count('rating'))['count_review']

    @property
    def count_albums(self):
        return self.albums.aggregate(count_albums=Count('id'))['count_albums']

    @property
    def approve_index(self):
        r = self.reviews.filter(rating__gte = 61).aggregate(approve=Count('rating'))['approve']
        if r == None:
            r = 0

        a = self.reviews.aggregate(count_review=Count('rating'))['count_review']

        if a != 0:
            a_i = round((r/a) * 100)
        else:
            a_i = 0

        return a_i

    @property
    def disapprove_index(self):
        r = self.reviews.filter(rating__lte = 59).aggregate(disapprove=Count('rating'))['disapprove']
        if r == None:
            r = 0

        a = self.reviews.aggregate(count_review=Count('rating'))['count_review']

        if a != 0:
            d_i = round((r/a) * 100)
        else:
            d_i = 0
    
        return d_i

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
        if self.reviews.aggregate(count_review=Count('rating'))['count_review'] > 4: 
            r = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
            r = round(r)
        else:
            r = -1
        return r

    @property
    def count_review(self):
        return self.reviews.aggregate(count_review=Count('rating'))['count_review']

    @property
    def approve_index(self):
        r = self.reviews.filter(rating__gte = 61).aggregate(approve=Count('rating'))['approve']
        if r == None:
            r = 0

        a = self.reviews.aggregate(count_review=Count('rating'))['count_review']

        if a != 0:
            a_i = round((r/a) * 100)
        else:
            a_i = 0

        return a_i

    @property
    def disapprove_index(self):
        r = self.reviews.filter(rating__lte = 59).aggregate(disapprove=Count('rating'))['disapprove']
        if r == None:
            r = 0

        a = self.reviews.aggregate(count_review=Count('rating'))['count_review']

        if a != 0:
            d_i = round((r/a) * 100)
        else:
            d_i = 0
    
        return d_i

    @property
    def tracks(self):
        return self.tracklist.aggregate(tracks=Count('id'))['tracks']

    def genre_list(self):
        return ', '.join([a.name for a in self.genre.all()])
    genre_list.short_description = "Genres"

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.username,
            "image": self.image,
            "artist": self.artist.name,
            "tracks": self.tracks,
            "genre": self.genre_list,
            "count_review": self.count_review,
            "rating": self.rating,
	}
    
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
    rating = models.IntegerField(default=0)
    place_in_tracklist = models.IntegerField(default=0)

    @property
    def rating(self):
        r = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        r = round(r)
        if r is None:
            r = -1
        return r

    class Meta:
        ordering = ['-id']

    def __str__(self):
        if (self.featuring != '') and (self.featuring != None):
            return f'{self.name} (feat. {self.featuring})'
        else:
            return f'{self.name}'

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
        r = self.reviews.aggregate(avg_rating=Cast(Round(Avg('rating')), output_field=IntegerField()))['avg_rating']
        if r is None:
            r = 0
        return r

    @property
    def count_review(self):
        return self.reviews.aggregate(count_review=Count('rating'))['count_review']

    @property
    def approve_index(self):
        r = self.reviews.filter(rating__gte = 61).aggregate(approve=Count('rating'))['approve']
        if r == None:
            r = 0

        a = self.reviews.aggregate(count_review=Count('rating'))['count_review']

        if a != 0:
            a_i = round((r/a) * 100)
        else:
            a_i = 0

        return a_i

    @property
    def disapprove_index(self):
        r = self.reviews.filter(rating__lte = 59).aggregate(disapprove=Count('rating'))['disapprove']
        if r == None:
            r = 0

        a = self.reviews.aggregate(count_review=Count('rating'))['count_review']

        if a != 0:
            d_i = round((r/a) * 100)
        else:
            d_i = 0
    
        return d_i

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
    rating = models.IntegerField(default=0, null=True)

    @property
    def get_rating(self):
        r = self.parent_review.aggregate(avg_rating=Cast(Round(Avg('rating')), output_field=IntegerField()))['avg_rating']
        return r

    def save(self, *args, **kwarg):
        if self.pk == None:
            super(Review, self).save(*args, **kwarg)
        else:
            self.rating = self.get_rating
            super(Review, self).save(*args, **kwarg)
    
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

class List(models.Model):
    ALBUM = 'al'
    ARTIST = 'ar'
    TRACK = 'tr'
    MAGAZINE = 'ma'
    type_choices = [
    (ALBUM, 'Álbum'),
    (ARTIST, 'Artista'),
    (TRACK, 'Faixa'),
    (MAGAZINE, 'Revista'),]

    name = models.CharField(max_length=300)
    description = models.TextField(max_length=500)
    type = models.CharField(
        max_length=2,
        choices=type_choices,
        default=ALBUM,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

