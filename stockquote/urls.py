from django.conf.urls import url

from stockquote import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^quote/(.+)$', views.quote),
    url(r'^quotes/(.+)$', views.quotes),
]
