from django.db import models
from django.urls import reverse


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'customer_id': self.pk})


class Lesson(models.Model):
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время', null=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.customer_id}'

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'lesson_id': self.pk})
