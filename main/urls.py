from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('calendar/', calendar, name='calendar'),
    path('addlesson/<str:date>/<str:time>/', add_lesson1, name='add_lesson1'),
    path('addlesson/', add_lesson, name='add_lesson'),
    path('profile/<str:customer>/', profile, name='profile'),

]
