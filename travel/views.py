from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from .models import Itinerary, Profile


class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class FilterView(TemplateView):
    template_name = 'travel/filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = Profile.objects.get(user=self.request.user)
        context['itineraries'] = Itinerary.objects.distinct()
        return context

class ItineraryList(ListView):
    model = Itinerary
    paginate_by = 100
    template_name='index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FollowingItinerariesView(TemplateView):
    template_name = 'travel/following_itineraries.html'

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
