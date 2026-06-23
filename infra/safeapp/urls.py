
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index , name='index'),  
    path('register/', views.register , name='register'),
    path('dashboard/', views.dashboard , name='dashboard'), 
    path('emergency/', views.emergency , name='emergency'),
    path('submit_report/', views.submit_report, name='submit_report'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_page, name='login'),
    path('submit_dashboard_report/', views.submit_dashboard_report, name='submit_dashboard_report'),
    path('delete_report/<str:report_id>/', views.delete_report, name='delete_report'),
    path(
    'approve_compensation/<str:report_id>/',
    views.approve_compensation
),
] 

