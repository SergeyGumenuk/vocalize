from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name}'


class Lesson(models.Model):
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время', null=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.customer_id}'
