from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Neighbourhood(models.Model):
    neighbourhood_name=models.CharField(max_length=250)
    location=models.CharField(max_length=200)
    occupation_count=models.IntegerField()


    def __str__(self):
        return self.neighbourhood_name

class Business(models.Model):
    business_name=models.CharField(max_length=200)
    business_owner=models.ForeignKey(User)
    business_type=models.CharField(max_length=100)
    neighbourhood=models.ForeignKey(Neighbourhood)
    business_email=models.CharField(max_length=100)
    phone_number=models.IntegerField()

    def __str__(self):
        return self.business_name


class Profile(models.Model):
    name=models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to = 'articles/')
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    neighbourhood=models.ForeignKey(Neighbourhood, null=True)
    email=models.CharField(max_length=100)
    email_confirmed=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

@receiver(post_save, sender=User)
def update_user_profile(sender,instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Message(models.Model):
    message=models.CharField(max_length=1000)
    user=models.ForeignKey(User)
    profile=models.ForeignKey(Profile)
    hood=models.ForeignKey(Neighbourhood)

    def __str__(self):
        return self.message


