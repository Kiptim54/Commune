from django.contrib import admin
from .models import Profile, Business, Neighbourhood, Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Neighbourhood)
admin.site.register(Business)
admin.site.register(Message)