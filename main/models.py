from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


class Customer(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    email = models.EmailField(blank=True, unique=True, null=True, verbose_name='Email')
    phone = models.CharField(max_length=20, unique=True, null=True, verbose_name='Номер телефона')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

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


class MediaFile(models.Model):
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Клиент')
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    file = models.FileField(
        upload_to='uploads/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mp3'])],
        blank=True, null=True, verbose_name='Медиафайл'
    )

    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'

    def __str__(self):
        return f'Файл - {self.customer_id}'

    def get_absolute_url(self):
        return reverse('media_file', kwargs={'media_file_id': self.pk})
