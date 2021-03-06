from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    url(r'^$', views.index_page, name='landingpage'),
    url(r'^search/', views.search_business, name='search_business'),
    url(r'^createprofile/$', views.create_profile, name='createprofile'),
    url(r'^neighbours/$', views.see_neighbours, name='see_neighbours'),
    url(r'neighbourhood/$', views.create_neighbourhood, name='create_neighbourhood'),
    url(r'business/$', views.create_business, name='create_business'),
    url(r'^message/$', views.send_message, name='send_message'),
    url(r'profile/$', views.view_profile, name='view_profile'),
    url(r'alerts/$', views.view_messages, name='view_messages'),
    url(r'businesses/$', views.view_businesses, name='view_businesses'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'profile/(?P<id>\d+)', views.business_profile, name='business_profile'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)