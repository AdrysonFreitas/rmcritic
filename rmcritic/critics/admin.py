from django.contrib import admin

from .models import Genre,Artist,Album,Magazine,Review,Track,ReviewTrack

admin.site.register(Track)
admin.site.register(ReviewTrack)

class GenreAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Genre, GenreAdmin)

class ArtistAdmin(admin.ModelAdmin):
    fields = ['name', 'image','country','genre']
    list_display = ('name','avg')
    list_filter = ['genre','country']
    search_fields = ['name']

admin.site.register(Artist, ArtistAdmin)

class TrackInline(admin.TabularInline):
    model = Track
    extra = 1

class AlbumAdmin(admin.ModelAdmin):
    fields = ['name', 'image','artist','genre']
    list_display = ('name','artist','rating')
    inlines = [TrackInline]
    list_filter = ['genre','artist']
    search_fields = ['name']

admin.site.register(Album, AlbumAdmin)

class MagazineAdmin(admin.ModelAdmin):
    fields = ['name', 'image','alt_name','adm','isActive']
    list_display = ('name','adm','avg','isActive')
    list_filter = ['isActive']
    search_fields = ['name']

admin.site.register(Magazine, MagazineAdmin)

class TrackReviewInline(admin.TabularInline):
    model = ReviewTrack
    extra = 1

class ReviewAdmin(admin.ModelAdmin):
    fields = ['magazine', 'album','artist','rating']
    list_display = ('album','magazine','rating')
    inlines = [TrackReviewInline]
    list_filter = ['magazine','artist','album']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['magazine'].queryset = Magazine.objects.filter(isActive=True)
        return super(ReviewAdmin, self).render_change_form(request, context, args, kwargs) 



admin.site.register(Review, ReviewAdmin)