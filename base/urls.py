from django.urls import path 
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name ='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', JobList.as_view(), name='jobs'),
    path('job/<int:pk>', JobDetail.as_view(), name='job'),
    path('job-create', create_job, name='job-create'),
    path('job-edit/<int:pk>', edit_job, name='job-edit'),
    path('job-delete/<int:pk>', delete_job, name='job-delete'),
]