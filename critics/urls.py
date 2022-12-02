from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('artists/', views.ArtistIndexView.as_view(), name='artist_index'),
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('magazines/', views.MagazineIndexView.as_view(), name='magazine_index'),
    path('magazine/<int:pk>/', views.MagazineDetailView.as_view(), name='magazine_detail'),
    path('lists/', views.ListIndexView.as_view(), name='list_index'),
    path('list/<int:pk>/', views.ListDetailView.as_view(), name='list_detail'),

]