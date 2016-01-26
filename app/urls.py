from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^portfolio/$', views.portfolio , name='portfolio'),
    url(r'^marketwatch/$', views.marketwatch , name='marketwatch'),
    url(r'^rules/$', views.rules , name='rules'),
    url(r'^ranking/$', views.ranking , name='ranking'),
    url(r'^buystock/$', views.buyStock , name='buyStock'),
    url(r'^sellstock/$', views.sellStock , name='sellStock'),
    url(r'^stockdetails/$', views.stockDetails , name='stockDetails'),
]
