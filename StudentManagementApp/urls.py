from django.urls import path, include

from StudentManagementApp import views

urlpatterns = [
    path('', views.view_login),
    path('register/', views.view_register),
    path('profile/', views.view_profile),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('forgot-password.html', views.forgetPassword),
    path('home/', views.loadHome),
    path('home/table.html', views.loadTable),
    path('home/logout/', views.doLogout),
    path('home/blank', views.blank),
    path('404/', views.load404)
]
