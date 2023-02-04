from django.urls import path

from profiles import views

urlpatterns = [
    path('customers/', views.ShowCustomers.as_view(), name='customers'),
    path('addcustomer/', views.AddCustomer.as_view(), name='add_customer'),
    path('<int:customer_id>/delete/', views.DeleteProfile.as_view(), name='delete_profile'),
    path('profile/<int:customer_id>/', views.ShowProfile.as_view(), name='profile'),
    path('addmediafile/<int:customer_id>/', views.AddMediaFile.as_view(), name='add_media_file'),
    path('mediafile/<int:media_file_id>', views.ShowMediaFile.as_view(), name='media_file'),
    path('<int:media_file_id>/deletemediafile/', views.DeleteMediaFile.as_view(), name='delete_media_file'),
]
