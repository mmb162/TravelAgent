from django.urls import path

from . import views

urlpatterns = [
    path('', views.ItineraryList.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('itinerary/following/', views.FollowingItinerariesView.as_view(), name='itinerary-following'),
    path('profile/<slug:slug>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('itinerary/add/', views.ItineraryCreateView.as_view(), name='itinerary-add'),
    path('itinerary/<slug:slug>/', views.ItineraryDetailView.as_view(), name='itinerary-detail')
]