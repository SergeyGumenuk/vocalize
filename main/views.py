import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from .forms import CalendarForm, AddLessonForm, AddLessonQuickForm, AddCustomerForm
from .models import *
from .forms import TIME_SLOTS


class LoginUser(LoginView):
    form_model = AuthenticationForm
    template_name = 'main/login.html'


class AddCustomer(LoginRequiredMixin, CreateView):
    template_name = 'main/add_profile.html'
    form_class = AddCustomerForm
    success_url = reverse_lazy('customers')


class ShowCustomers(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'main/customers.html'
    context_object_name = 'customers'


def logout_user(request):
    logout(request)
    return redirect('home')


def index(request):
    return render(request, 'main/base.html', {'title': 'Главная страница'})


# class Calendar(ListView):
#     model = Lesson
#     template_name = 'main/calendar.html'
#     context_object_name = 'lessons'
#
#     def get_queryset(self, request):
#         if request.method == 'post':
#             lessons = Lesson.objects.filter(date=request.POST['date'])
#         else:
#             lessons = Lesson.objects.filter(date=datetime.date.today())
#         return lessons
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_slots'] = TIME_SLOTS
#         context['title'] = 'Календарь'
#         return context
@login_required
def calendar(request):
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
    return render(request, 'main/calendar.html', context=context)


@login_required
def add_lesson(request):
    form = AddLessonForm()
    if request.method == 'POST':
        Lesson.objects.create(date=request.POST['date'],
                              time=request.POST['time'],
                              customer_id=Customer.objects.get(pk=request.POST['customer_id']))
        return redirect(reverse_lazy('calendar'))
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


class ShowLesson(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'main/lesson.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'

# @login_required
# def show_lesson(request, lesson_id):
#     lesson = Lesson.objects.get(pk=lesson_id)
#     context = {
#         'lesson': lesson
#     }
#     return render(request, 'main/lesson.html', context=context)


class DeleteLesson(LoginRequiredMixin, DeleteView):
    model = Lesson
    success_url = reverse_lazy('calendar')
    pk_url_kwarg = 'lesson_id'

# @login_required
# def delete_lesson(request, lesson_id):
#     Lesson.objects.filter(pk=lesson_id).delete()
#     return redirect(reverse_lazy('calendar'))


class ShowProfile(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'main/profile.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'customer_id'

# @login_required
# def show_profile(request, customer_id):
#     customer = Customer.objects.get(pk=customer_id)
#     context = {
#         'customer': customer
#     }
#     return render(request, 'main/profile.html', context=context)


class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')
    pk_url_kwarg = 'customer_id'

# @login_required
# def delete_profile(request, customer_id):
#     Customer.objects.filter(pk=customer_id).delete()
#     return redirect(reverse_lazy('customers'))
