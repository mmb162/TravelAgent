from django.urls import path

from . import views

urlpatterns = [
    path('', views.ItineraryList.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('following/', views.FollowingUsersView.as_view(), name='following-users'),
    path('profile/<slug:slug>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/update', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('itinerary/add/', views.ItineraryCreateView.as_view(), name='itinerary-add'),
    path('itinerary/<slug:slug>/', views.ItineraryDetailView.as_view(), name='itinerary-detail')
]

# requests
urlpatterns += [
    path('follow-user/', views.FollowUser, name='follow-user'),
    path('save-itinerary/', views.SaveItinerary, name='save-itinerary'),
    path('filter/', views.FilterView.as_view(), name="filter"),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
]