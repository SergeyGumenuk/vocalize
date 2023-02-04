from django.urls import path

from appointments import views

urlpatterns = [
    path('calendar/', views.calendar, name='calendar'),
    path('addlesson/<str:date>/<str:time>/', views.add_lesson_quick, name='add_lesson_quick'),
    path('addlesson/', views.add_lesson, name='add_lesson'),
    path('<int:lesson_id>/delete_lesson/', views.DeleteLesson.as_view(), name='delete_lesson'),
    path('lesson/<int:lesson_id>/', views.ShowLesson.as_view(), name='lesson'),
]
