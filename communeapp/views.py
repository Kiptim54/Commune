from django.shortcuts import render, HttpResponse


# Create your views here.
def index_page(request):
    '''
    function to call method in the 
    landing page
    '''
    return HttpResponse("welcome to commune!")