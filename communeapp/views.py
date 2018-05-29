from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, get_object_or_404, get_list_or_404, Http404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import SignUpForm, Creatprofileform, Createneighbourhood, BusinessForm, MessageForm
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .models import Profile, Message, Neighbourhood, Business
from django.contrib.auth.decorators import login_required


# Create your views here.
def index_page(request):
    '''
    function to call method in the 
    landing page
    '''
    title="Commune | Home"
    current_user=request.user
    current_user.id=request.user.id
    print("hello")
    if not current_user.is_authenticated():
        return redirect('login')
    else:
        allprofiles=Profile.objects.all()
        profile=Profile.objects.filter(user=current_user)
    return render(request, 'watch/index.html' ,{"title":title, "profile":profile, "profile":allprofiles, "id":current_user.id})


def view_profile(request):
    '''
    funtion for viewing a user's profile
    '''
    title="Commune | Profile "
    current_user=request.user.id
    if not Profile.objects.filter(user=current_user).exists():
        return redirect('createprofile')
    else:
        profile=Profile.objects.filter(user=current_user)
    return render(request, 'views/profile.html', {"profile":profile, "title":title})

def view_messages(request):
    '''
    function for viewing messages posted to neighbourhood
    '''
    title="Commune | Alerts "
    current_user=request.user
    neighbours=Profile.objects.get(user=current_user)
    neighbourhood=neighbours.neighbourhood
    message=Message.objects.filter(hood=neighbourhood)
    message=message.reverse()
    print(neighbourhood)
    return render(request, 'views/messages.html', {"title":title, "messages":message, "hood":neighbourhood})

def view_businesses(request):
    '''
    function for viewing all businesses in one's neighbourhood
    '''
    title="Commune | Business"
    current_user=request.user
    current_user.id=request.user.id
    neighbours=Profile.objects.get(user=current_user)
    neighbourhood=neighbours.neighbourhood
    businesses=Business.objects.filter(neighbourhood=neighbourhood)
    profile=Profile.objects.all()
    print(profile)
    profile_id=profile
    # selected_profile=get_list_or_404(Profile,id=profile)
    # final=selected_profile.id
    # print(final)
    
    # print(selected_profile)
    
    return render(request, 'views/business.html', {"title":title, "hood":neighbourhood, "businesses":businesses})

def business_profile(request, id):
    '''
    function for to show one's profile with their id on the url
    '''
    title="Commune | Profile "
    current_user=request.user.id
    id_profile=get_object_or_404(Profile, id=id)
    print(id_profile)
    if not Profile.objects.filter(user=current_user).exists():
        return redirect('createprofile')
    else:
        profile=Profile.objects.filter(user=current_user)
    return render(request, 'views/id-profile.html', {"profile":id_profile, "title":title ,"id":id})
    
    

def search_business(request):
    '''
    function that searching for all businesses
    '''
    if 'business' in request.GET and request.GET['business']:
        search_term=request.GET.get('business')
        searched_business=Business.search_business(search_term)
        message=f'{search_term}'

        return render(request, 'views/searched_business.html', {"message":message, "businesses":searched_business})

def see_neighbours(request):
    '''
    views to see all your neighbours
    '''
    title="Commune | Neighbours"
    current_user=request.user
    profile_email=current_user.email
    # profile_id=get_object_or_404(Profile, id=id)
    # print(profile_id)
    profile=Profile.objects.all().get(email=profile_email)
    print(profile)
    neighbourhood=profile.neighbourhood
    print(neighbourhood)
    neighbours=Profile.objects.filter(neighbourhood=neighbourhood)
    print(neighbours)
    return render(request, 'views/neighbours.html', {"neighbours":neighbours})


@login_required(login_url='/login/')
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
            return redirect('view_profile')
    else:
        form=Creatprofileform()
    return render(request, 'watch/create_profile.html', {"title":title, "form":form})

@login_required(login_url='/login/')
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
            return redirect('createprofile')
    else:
        form=Createneighbourhood()
    return render(request, 'watch/neighbourhood_profile.html', {"title":title, "form":form})
@login_required(login_url='/login/')
def create_business(request):
    '''
    function to create business in 
    a  neighbourhood
    '''
    current_user=request.user
    title="Commune | Business " 
    if request.method=='POST':
        form=BusinessForm(request.POST)
        if form.is_valid():
            business=form.save(commit=False)
            business.business_owner=current_user
            business.save()
            return redirect('view_businesses')
    else:
        form=BusinessForm()
    return render(request, 'watch/business_profile.html', {"title":title, "form":form})
    
@login_required(login_url='/login/')
def send_message(request):
    '''
    function for neighbours to share messages with 
    each other
    '''
    current_user=request.user
    title="Commune | Message"
    profile=Profile.objects.get(user=current_user)
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.user=current_user
            message.profile=profile
            message.hood=profile.neighbourhood
            message.save()
            return redirect('view_messages')
    else:
        form=MessageForm()

    return render(request, 'watch/send_message.html', {"form":form, "title":title})


def signup(request):
    '''
    function that signs up a new user
    '''

    title="Commune | Sign Up"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print(user)
            current_site = get_current_site(request)
            subject = 'Activate Your Commune Account'
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
    return render(request, 'registration/signup.html', {'form': form, "title":title})

def activate(request, uidb64, token):
    '''
    function activates a user and allows then to 
    start using the account
    '''
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
        return redirect('createprofile')
    else:
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    '''
    function that redirects to template
    that tells users an email has been sent to them
    '''
    current_user=request.user
    # if current_user.is_authenticated:
    #     return redirect('account_activation_sent')
    title='Commune | confirm email'
    return render(request, 'email/account_activation_sent.html', {"title":title})




