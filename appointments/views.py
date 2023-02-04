import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView

from appointments.models import Lesson
from main.forms import CalendarForm, TIME_SLOTS, AddLessonForm, AddLessonQuickForm

from profiles.models import Customer


@login_required
def calendar(request):
    """Функция выводит на экран выбранную дату и уроки, назначенные на эту дату"""
    if request.method == 'POST':
        form = CalendarForm(request.POST)
        date = request.POST['date']
        lessons = Lesson.objects.filter(date=request.POST['date']).select_related('customer_id')
    else:
        form = CalendarForm()
        date = datetime.date.today()
        lessons = Lesson.objects.filter(date=datetime.date.today()).select_related('customer_id')
    context = {
        'title': 'Календарь',
        'lessons': lessons,
        'form': form,
        'time_slots': TIME_SLOTS,
        'date': date
    }
    return render(request, 'appointments/calendar/calendar.html', context=context)


@login_required
def add_lesson(request):
    """Функция добавляет урок в календарь на указанную дату"""
    form = AddLessonForm()
    if request.method == 'POST':
        Lesson.objects.create(date=request.POST['date'],
                              time=request.POST['time'],
                              customer_id=Customer.objects.get(pk=request.POST['customer_id']))
        return redirect(reverse_lazy('calendar'))
    return render(request, 'appointments/lessons/add_lesson.html', {'form': form})


@login_required
def add_lesson_quick(request, date, time):
    """Функция добавляет урок на указанное в интерфейсе время выведенной на экран даты"""
    form = AddLessonQuickForm()
    if request.method == 'POST':
        if Lesson.objects.filter(date=date, time=time).exists():
            return redirect(reverse_lazy('calendar'))
        else:
            Lesson.objects.create(date=date,
                                  time=time,
                                  customer_id=Customer.objects.get(pk=request.POST['customer_id']))
        return redirect(reverse_lazy('calendar'))
    return render(request, 'appointments/lessons/add_lesson.html', {'form': form})


class ShowLesson(LoginRequiredMixin, DetailView):
    """Класс для отображения конкретного урока по его id"""
    model = Lesson
    template_name = 'appointments/lessons/lesson.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'


class DeleteLesson(LoginRequiredMixin, DeleteView):
    """Класс для удаления урока"""
    model = Lesson
    template_name = 'appointments/lessons/lesson_confirm_delete.html'
    success_url = reverse_lazy('calendar')
    pk_url_kwarg = 'lesson_id'
