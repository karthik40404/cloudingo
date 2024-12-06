from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    # path('files/', views.list_files, name='list_files'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('files/', views.file_list, name='list_files'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
]
