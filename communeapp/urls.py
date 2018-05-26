from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    url(r'^$', views.index_page, name='landingpage'),
    url(r'^createprofile/$', views.create_profile, name='createprofile'),
    url(r'neighbourhood/$', views.create_neighbourhood, name='create_neighbourhood'),
    url(r'business/$', views.create_business, name='create_business'),
    url(r'^message/$', views.send_message, name='send_message'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)