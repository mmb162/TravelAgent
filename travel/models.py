from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    slug = models.SlugField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    biography = models.TextField(blank=True)
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    saved_itineraries = models.ManyToManyField('Itinerary', blank=True, related_name='saves')

    def __str__(self):
        return self.user.get_username()
    
    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'slug': self.slug})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    prof = instance.profile
    prof.slug = slugify(prof.user.get_username())
    prof.save()


class Itinerary(models.Model):
    BUDGET_CHOICES = [
        ('Less than $500', 'Less than $500'),
        ('$500-1000', '$500-1000'),
        ('$1000-2000', '$1000-2000'),
        ('More than $2000', 'More than $2000'),
    ]
    TRIP_LENGTH_CHOICES = [
        ('Less than 1 week', 'Less than 1 week'),
        ('1 week', '1 week'),
        ('2 weeks', '2 weeks'),
        ('3 weeks', '3 weeks'),
        ('4 weeks', '4 weeks'),
        ('More than 1 month', 'More than 1 month')
    ]
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    ]
    CLIMATE_CHOICES = [
        ('Tropical', 'Tropical'),
        ('Dry', 'Dry'),
        ('Temperate', 'Temperate'),
        ('Continental', 'Continental'),
        ('Polar', 'Polar')
    ]
    name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(unique=True)
    picture = models.ImageField(upload_to='itinerary_pictures/', blank=False)
    description = models.TextField(blank=True)
    budget = models.CharField(max_length=15, choices=BUDGET_CHOICES, default='Less than $500')
    trip_length = models.CharField(max_length=17, choices=TRIP_LENGTH_CHOICES, default='Less than 1 week')
    month = models.CharField(max_length=9, choices=MONTH_CHOICES, default='JANUARY')
    climate = models.CharField(max_length=11, choices=CLIMATE_CHOICES, default='TROPICAL')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('itinerary-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
