from django.urls import path

from core.views import *

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('news/', IndexView.as_view(), name='news'),
    path('news/papers/', IndexView.as_view(), name='news_papers'),
    path('about/', IndexView.as_view(), name='about'),
    path('about/us/', IndexView.as_view(), name='about_us'),
    path('about/you/', IndexView.as_view(), name='about_you'),
    path('about/them/', IndexView.as_view(), name='about_them'),
]
