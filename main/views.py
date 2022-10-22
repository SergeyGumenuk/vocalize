import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import CalendarForm, AddLessonForm, AddLessonQuickForm, AddCustomerForm
from .models import *
from .forms import TIME_SLOTS


class LoginUser(LoginView):
    form_model = AuthenticationForm


def logout_user(request):
    logout(request)
    return redirect('home')


def index(request):
    return render(request, 'main/base.html', {'title': 'Главная страница'})


@login_required
def calendar(request):
    if request.method == 'POST':
        form = CalendarForm(request.POST)
        date = request.POST['date']
        lessons = Lesson.objects.filter(date=request.POST['date'])
    else:
        form = CalendarForm()
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


@login_required
def add_lesson(request):
    form = AddLessonForm()
    if request.method == 'POST':
        Lesson.objects.create(date=request.POST['date'],
                              time=request.POST['time'],
                              customer_id=Customer.objects.get(pk=request.POST['customer_id']))

    return render(request, 'main/add_lesson.html', {'form': form})


@login_required
def add_lesson_quick(request, date, time):
    form = AddLessonQuickForm()
    if request.method == 'POST':
        if Lesson.objects.filter(date=date, time=time).exists():
            return redirect(reverse_lazy('calendar'))
        else:
            Lesson.objects.create(date=date,
                                  time=time,
                                  customer_id=Customer.objects.get(pk=request.POST['customer_id']))
        return redirect(reverse_lazy('calendar'))
    return render(request, 'main/add_lesson.html', {'form': form})


class AddCustomer(LoginRequiredMixin, CreateView):
    template_name = 'main/add_profile.html'
    form_class = AddCustomerForm
    success_url = reverse_lazy('customers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ShowCustomers(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'main/customers.html'
    context_object_name = 'customers'


@login_required
def delete_lesson(request, lesson_id):
    Lesson.objects.filter(pk=lesson_id).delete()
    return redirect(reverse_lazy('calendar'))


@login_required
def delete_profile(request, customer_id):
    Customer.objects.filter(pk=customer_id).delete()
    return redirect(reverse_lazy('customers'))


@login_required
def show_profile(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)
    context = {
        'customer': customer
    }
    return render(request, 'main/profile.html', context=context)


@login_required
def show_lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    context = {
        'lesson': lesson
    }
    return render(request, 'main/lesson.html', context=context)
