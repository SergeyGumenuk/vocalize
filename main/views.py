import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from .forms import CalendarForm, AddLessonForm, AddLessonQuickForm, AddCustomerForm, AddMediaFileForm
from .models import *
from .forms import TIME_SLOTS


class LoginUser(LoginView):
    """Класс, реализующий вход пользователя"""
    form_model = AuthenticationForm
    template_name = 'main/login.html'


class AddCustomer(LoginRequiredMixin, CreateView):
    """Класс для добавления клиента в систему"""
    template_name = 'main/add_profile.html'
    form_class = AddCustomerForm
    success_url = reverse_lazy('customers')


class ShowCustomers(LoginRequiredMixin, ListView):
    """Класс для отображения списка всех клиентов"""
    model = Customer
    template_name = 'main/customers.html'
    context_object_name = 'customers'


class ShowLesson(LoginRequiredMixin, DetailView):
    """Класс для отображения конкретного урока по его id"""
    model = Lesson
    template_name = 'main/lesson.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'


class DeleteLesson(LoginRequiredMixin, DeleteView):
    """Класс для удаления урока"""
    model = Lesson
    success_url = reverse_lazy('calendar')
    pk_url_kwarg = 'lesson_id'


class ShowProfile(LoginRequiredMixin, DetailView):
    """Клас для отображеня профиля клиента по его id"""
    model = Customer
    template_name = 'main/profile.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'customer_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_files'] = context['customer'].mediafile_set.all()
        return context


class DeleteProfile(LoginRequiredMixin, DeleteView):
    """Класс для удаления клиента из системы"""
    model = Customer
    success_url = reverse_lazy('customers')
    pk_url_kwarg = 'customer_id'


class AddMediaFile(LoginRequiredMixin, CreateView):
    """Класс для добавления аудио или видио на страницу профиля клиента"""
    form_class = AddMediaFileForm
    template_name = 'main/add_media_file.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['customer_id'] = self.kwargs['customer_id']
        return initial


class ShowMediaFile(LoginRequiredMixin, DetailView):
    """Класс для отображения конкретного файла клиента по его id"""
    model = MediaFile
    template_name = 'main/media_file.html'
    pk_url_kwarg = 'media_file_id'
    context_object_name = 'media_file'


class DeleteMediaFile(LoginRequiredMixin, DeleteView):
    """Класс для удаления аудио или видео файла по его id"""
    model = MediaFile
    pk_url_kwarg = 'media_file_id'

    def get_success_url(self):
        customer = Customer.objects.get(pk=self.object.customer_id.pk)
        return reverse('profile', kwargs={'customer_id': customer.pk})


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
    return render(request, 'main/calendar.html', context=context)


@login_required
def add_lesson(request):
    """Функция добавляет урок в календарь на указанную дату"""
    form = AddLessonForm()
    if request.method == 'POST':
        Lesson.objects.create(date=request.POST['date'],
                              time=request.POST['time'],
                              customer_id=Customer.objects.get(pk=request.POST['customer_id']))
        return redirect(reverse_lazy('calendar'))
    return render(request, 'main/add_lesson.html', {'form': form})


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
    return render(request, 'main/add_lesson.html', {'form': form})


def logout_user(request):
    """Функция осуществляет выход пользователя из системы"""
    logout(request)
    return redirect('home')


def index(request):
    """Функция выводит главную страницу"""
    return render(request, 'main/base.html', {'title': 'Главная страница'})