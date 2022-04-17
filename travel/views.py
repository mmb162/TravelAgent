from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
import json

from .models import Itinerary, Profile


class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class ItineraryList(ListView):
    model = Itinerary
    paginate_by = 100
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = Profile.objects.get(user=self.request.user)
        context['following'] = current_user.follows.all()
        context['saved'] = current_user.saved_itineraries.all()
        return context


class FollowingUsersView(TemplateView):
    template_name = 'travel/following_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = Profile.objects.get(user=self.request.user)
        context['itineraries'] = Itinerary.objects.filter(created_by__in=current_user.follows.all()).distinct()
        return context


class ItineraryCreateView(LoginRequiredMixin, CreateView):
    model = Itinerary
    success_url = reverse_lazy('index')
    fields = ['name', 'description', 'budget', 'trip_length', 'month', 'climate']

    def form_valid(self, form):
        form.instance.created_by = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class ItineraryDetailView(DetailView):
    model = Itinerary
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileDetailView(DetailView):
    model = Profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['published'] = Itinerary.objects.filter(created_by=self.object).all()
        return context


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['profile_picture', 'biography']

    def get_object(self, **kwargs):
        return Profile.objects.get(user=self.request.user)

def FollowUser(request):
    data = json.loads(request.body)
    if request.method=='POST':
        toFollowUser = User.objects.get(username=data['userToFollow'])
        if not toFollowUser:
            return HttpResponse("This user does not exist.")
        toFollowProfile = Profile.objects.get(user=toFollowUser)
        if not toFollowProfile:
            return HttpResponse("This user does not exist.")
        currentProfile = Profile.objects.get(user=request.user)
        if currentProfile.follows.filter(pk=toFollowProfile.pk).exists():
            return HttpResponse("You already follow this user.")
        currentProfile.follows.add(toFollowProfile)
    return HttpResponse(200)

def SaveItinerary(request):
    data = json.loads(request.body)
    if request.method=='POST':
        itinerary = Itinerary.objects.get(name=data['itinerary'])
        if not itinerary:
            return HttpResponse("This itinerary does not exist.")
        currentProfile = Profile.objects.get(user=request.user)
        if currentProfile.saved_itineraries.filter(pk=itinerary.pk).exists():
            return HttpResponse("You already saved this itinerary.")
        currentProfile.saved_itineraries.add(itinerary)
    return HttpResponse(200)