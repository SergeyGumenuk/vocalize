import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import Calendar, AddLessonForm, AddLessonForm1
from .models import *
from .forms import TIME_SLOTS


def index(request):
    return render(request, 'main/base.html', {'title': 'Главная страница'})


def calendar(request):
    form = Calendar()
    if request.method == 'POST':
        date = request.POST['date']
        lessons = Lesson.objects.filter(date=request.POST['date'])
    else:
        date = datetime.date.today()
        lessons = Lesson.objects.filter(date=datetime.date.today())
    context = {
        'title': 'Календарь',
        'lessons': lessons,
        'form': form,
        'time_slots': TIME_SLOTS,
        'date': date

    }
    return render(request, 'main/calendar.html', context=context)


def add_lesson(request):
    form = AddLessonForm()
    if request.method == 'POST':
        print(request.POST)
        Lesson.objects.create(date=request.POST['date'],
                              time=request.POST['time'],
                              customer_id=Customer.objects.get(pk=request.POST['customer_id']))

    return render(request, 'main/add_lesson.html', {'form': form})


def add_lesson1(request, date, time):
    form = AddLessonForm1()
    if request.method == 'POST':
        Lesson.objects.create(date=date,
                              time=time,
                              customer_id=Customer.objects.get(pk=request.POST['customer_id']))

    return render(request, 'main/add_lesson.html', {'form': form})


def profile(request, customer):
    customer = Customer.objects.get(name=customer)
    context = {
        'customer': customer
    }
    return render(request, 'main/profile.html', context=context)
