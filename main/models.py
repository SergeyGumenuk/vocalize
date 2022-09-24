from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} {self.surname}'


class Lesson(models.Model):
    date = models.DateField(verbose_name='Дата')
    customer_id = models.ForeignKey('Customer', on_delete=models.PROTECT, verbose_name='Клиент')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'{self.customer_id} {self.date}'
