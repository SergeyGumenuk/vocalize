from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('calendar/', calendar, name='calendar'),
    path('addlesson/<str:date>/<str:time>/', add_lesson_quick, name='add_lesson1'),
    path('addlesson/', add_lesson, name='add_lesson'),
    path('customers/', ShowCustomers.as_view(), name='customers'),
    path('addcustomer/', AddCustomer.as_view(), name='add_customer'),
    path('delete/<int:customer_id>/', delete_profile, name='delete_profile'),
    path('delete_lesson/<int:lesson_id>/', delete_lesson, name='delete_lesson'),
    path('lesson/<int:lesson_id>/', show_lesson, name='lesson'),
    path('profile/<int:customer_id>/', show_profile, name='profile'),  # Fix it to slug

]
