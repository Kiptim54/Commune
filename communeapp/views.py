from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm, Creatprofileform, Createneighbourhood
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
@login_required
def index_page(request):
    '''
    function to call method in the 
    landing page
    '''
    title="Commune | Home"
    return render(request, 'watch/index.html' ,{"title":title})

@transaction.atomic
def create_profile(request):
    '''
    function that saves users profile
    '''
    title="Commune | Create Profile"
    try:
        profile=Profile.objects.get(user=request.user)
    except profile.DoesNotExist:
        profile =Profile(user=request.user)
    current_user=request.user
    if request.method=='POST':
        form=Creatprofileform(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=current_user
            profile.save()
    else:
        form=Creatprofileform()
    return render(request, 'watch/create_profile.html', {"title":title, "form":form})

def create_neighbourhood(request):
    '''
    function for user to create neighbourhood
    '''
    title='Commune | Neighbourhood'
    current_user=request.user
    if request.method=='POST':
        form=Createneighbourhood(request.POST)
        if form.is_valid():
            neighbourhood=form.save(commit=False)
            neighbourhood.save()
    else:
        form=Createneighbourhood()
    return render(request, 'watch/neighbourhood_profile.html', {"title":title, "form":form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print(user)
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    current_user=request.user
    # if current_user.is_authenticated:
    #     return redirect('account_activation_sent')
    title='Commune | confirm email'
    return render(request, 'email/account_activation_sent.html', {"title":title})




