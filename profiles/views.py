from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from main.forms import AddCustomerForm, AddMediaFileForm
from profiles.models import Customer, MediaFile


class AddCustomer(LoginRequiredMixin, CreateView):
    """Класс для добавления клиента в систему"""
    template_name = 'profiles/profile/add_profile.html'
    form_class = AddCustomerForm
    success_url = reverse_lazy('customers')


class ShowCustomers(LoginRequiredMixin, ListView):
    """Класс для отображения списка всех клиентов"""
    model = Customer
    template_name = 'profiles/profile/customers.html'
    context_object_name = 'customers'


class ShowProfile(LoginRequiredMixin, DetailView):
    """Клас для отображеня профиля клиента по его id"""
    model = Customer
    template_name = 'profiles/profile/profile.html'
    context_object_name = 'customer'
    pk_url_kwarg = 'customer_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_files'] = context['customer'].mediafile_set.all()
        return context


class DeleteProfile(LoginRequiredMixin, DeleteView):
    """Класс для удаления клиента из системы"""
    model = Customer
    template_name = 'profiles/profile/customer_confirm_delete.html'
    success_url = reverse_lazy('customers')
    pk_url_kwarg = 'customer_id'


class AddMediaFile(LoginRequiredMixin, CreateView):
    """Класс для добавления аудио или видио на страницу профиля клиента"""
    form_class = AddMediaFileForm
    template_name = 'profiles/files/add_media_file.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['customer_id'] = self.kwargs['customer_id']
        return initial


class ShowMediaFile(LoginRequiredMixin, DetailView):
    """Класс для отображения конкретного файла клиента по его id"""
    model = MediaFile
    template_name = 'profiles/files/media_file.html'
    pk_url_kwarg = 'media_file_id'
    context_object_name = 'media_file'


class DeleteMediaFile(LoginRequiredMixin, DeleteView):
    """Класс для удаления аудио или видео файла по его id"""
    model = MediaFile
    template_name = 'profiles/files/mediafile_confirm_delete.html'
    pk_url_kwarg = 'media_file_id'

    def get_success_url(self):
        customer = Customer.objects.get(pk=self.object.customer_id.pk)
        return reverse('profile', kwargs={'customer_id': customer.pk})
