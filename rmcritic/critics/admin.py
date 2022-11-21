from django.contrib import admin

from .models import Genre,Artist,Album,Magazine,Review,Track,ReviewTrack

@admin.action(description='Ativar revista')
def make_active(modeladmin, request, queryset):
    if queryset.filter(isActive=False):
        queryset.update(isActive=True)
    else:
        queryset.update(isActive=False)

class GenreAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Genre, GenreAdmin)

class ArtistAdmin(admin.ModelAdmin):
    fields = ['name', 'image','country','genre']
    list_display = ('name','avg')
    list_filter = ['genre','country']
    search_fields = ['name']

admin.site.register(Artist, ArtistAdmin)

class TrackAdmin(admin.ModelAdmin):
    fields = ['name', 'featuring','parent_album','place_in_tracklist']
    list_display = ('name','featuring','parent_album','rating')
    list_filter = ['parent_album__artist','parent_album']
    search_fields = ['name']

admin.site.register(Track,TrackAdmin)

class TrackInline(admin.TabularInline):
    model = Track
    fields = ('name', 'featuring', 'place_in_tracklist')
    extra = 1

class AlbumAdmin(admin.ModelAdmin):
    fields = ['name', 'image','artist','genre']
    list_display = ('name','artist','rating')
    inlines = [TrackInline]
    list_filter = ['genre','artist']
    search_fields = ['name']

admin.site.register(Album, AlbumAdmin)

class MagazineAdmin(admin.ModelAdmin):
    fields = ['name', 'image','alt_name','adm']
    list_display = ('name','adm','avg','isActive')
    list_filter = ['isActive']
    search_fields = ['name']
    actions = [make_active]

admin.site.register(Magazine, MagazineAdmin)

class TrackReviewInline(admin.TabularInline):
    model = ReviewTrack
    fields = ['track', 'rating']
    autocomplete_fields = ['track']
    extra = 1

class ReviewAdmin(admin.ModelAdmin):
    fields = ['magazine', 'album','artist','rating']
    list_display = ('album','magazine','rating')
    inlines = [TrackReviewInline]
    list_filter = ['magazine','artist','album']
    autocomplete_fields = ['magazine', 'album', 'artist']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['magazine'].queryset = Magazine.objects.filter(isActive=True)
        return super(ReviewAdmin, self).render_change_form(request, context, args, kwargs) 

admin.site.register(Review, ReviewAdmin)