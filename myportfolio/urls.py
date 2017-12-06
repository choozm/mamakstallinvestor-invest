from django.conf.urls import patterns, url
from myportfolio import views

urlpatterns = [
    url(r'^$', views.investor),
    url(r'^portfolio/(.+)$', views.portfolio),
    url(r'^transaction/(.+)$', views.transaction),
    ]
