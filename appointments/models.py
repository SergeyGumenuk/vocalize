from django.db import models
from django.urls import reverse

from profiles.models import Customer


class Lesson(models.Model):
    """Класс, хараутеризующий сущность урока"""
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время', null=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.customer_id}'

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'lesson_id': self.pk})
