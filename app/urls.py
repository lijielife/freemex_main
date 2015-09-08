from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^confirm/(?P<activation_key>\w+)/$',views.confirm,name='vendor_login'),
]
