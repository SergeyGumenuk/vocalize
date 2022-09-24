import datetime

from django.shortcuts import render
from django.utils.datetime_safe import date

from .forms import Calendar
from .models import *


def index(request):
    return render(request, 'main/base.html', {'title': 'Главная страница'})


def calendar(request):
    form = Calendar()
    if request.method == 'POST':
        lessons = Lesson.objects.filter(date=request.POST['date'])
    else:
        lessons = Lesson.objects.filter(date=datetime.date.today())
    context = {
        'title': 'Календарь',
        'lessons': lessons,
        'form': form

    }
    return render(request, 'main/calendar.html', context=context)
