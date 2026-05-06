from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_report, name='create_report'),
    
    path('report/<int:id>/', views.report_detail, name='report_detail'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),
]