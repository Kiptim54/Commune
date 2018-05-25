from django.test import TestCase
from .models import Profile, Neighbourhood, Business
from django.contrib.auth.models import User

user = User.objects.create_user("testuser", "secret")
class ProfileTestClass(TestCase):
    '''
    method to tests the profile functionality
    '''
   
    def setUp(self):
        '''
        function to setup a profile that will be 
        tested
        '''
        
        self_neighbour=Neighbourhood(neighbourhood_name='ngummo',location='kibera', occupation_count=7)
        self_neighbour.save()
        new_profile=Profile(name="Brenda Kiptim", profile_image='kkiki.jpg', user=user, neighbourhood=self_neighbour, email='kiptim54@gmail.com', email_confirmed=True,)
        new_profile.save()


    def test_save_profile(self):
        setUp(self)
        self.save_profile()
        profiles=Profile.objects.all()
        self.assertTrue(len(profiles)>0)


    #  Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))

    def tearDown(self):
        '''
        function to delete all the items in the setup
        '''
        Profile.objects.all().delete()
        Neighbourhood.objects.all().delete()
        Business.objects.all().delete()
       

