from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('calendar/', calendar, name='calendar'),
    path('addlesson/<str:date>/<str:time>/', add_lesson_quick, name='add_lesson_quick'),
    path('addlesson/', add_lesson, name='add_lesson'),
    path('customers/', ShowCustomers.as_view(), name='customers'),
    path('addcustomer/', AddCustomer.as_view(), name='add_customer'),
    path('<int:customer_id>/delete/', DeleteProfile.as_view(), name='delete_profile'),
    path('<int:lesson_id>/delete_lesson/', DeleteLesson.as_view(), name='delete_lesson'),
    path('lesson/<int:lesson_id>/', ShowLesson.as_view(), name='lesson'),
    path('profile/<int:customer_id>/', ShowProfile.as_view(), name='profile'),
    path('addmediafile/<int:customer_id>/', AddMediaFile.as_view(), name='add_media_file'),
    path('mediafile/<int:media_file_id>', ShowMediaFile.as_view(), name='media_file'),
    path('<int:media_file_id>/deletemediafile/', DeleteMediaFile.as_view(), name='delete_media_file')

]
