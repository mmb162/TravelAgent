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
from .models import Itinerary, Profile
from itertools import chain
import json
from django.db.models import Q 

class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class SearchResultsView(ListView):
    model = Itinerary
    template_name = 'travel/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        budgetquery = self.request.GET.get("budget")
        triplengthquery = self.request.GET.get("trip_length")
        monthquery = self.request.GET.get("month")
        climatequery = self.request.GET.get("climate")
        if(Itinerary.name != ""):
            object_list = Itinerary.objects.filter(Q(name__icontains=query))
        if(budgetquery != "Any Budget"):
            object_list = object_list & Itinerary.objects.filter(Q(budget__icontains=budgetquery))
        if(triplengthquery != "Any Trip Length"):
            object_list = object_list & Itinerary.objects.filter(Q(trip_length__icontains=budgetquery))
        if(monthquery != "Any Month"):
            object_list = object_list & Itinerary.objects.filter(Q(month__icontains=monthquery))
        if(climatequery != "Any Climate"):
            object_list = object_list & Itinerary.objects.filter(Q(climate__icontains=climatequery))
        return object_list

class FilterView(TemplateView):
    template_name = 'travel/filter.html'

class ItineraryList(LoginRequiredMixin, ListView):
    model = Itinerary
    paginate_by = 100
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FollowingUsersView(LoginRequiredMixin, TemplateView):
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


class ItineraryDetailView(LoginRequiredMixin, DetailView):
    model = Itinerary
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['published'] = Itinerary.objects.filter(created_by=self.object).all()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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

