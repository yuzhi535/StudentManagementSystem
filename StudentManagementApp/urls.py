from django.urls import path, include

from StudentManagementApp import views

urlpatterns = [
    path('', views.view_login, name='login'),
    path('register/', views.view_register),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('home/forgot-password.html', views.forgetPassword, name='forget'),
    path('home/', views.loadHome, name='home'),
    path('home/table.html', views.loadTable, name='table'),
    path('home/logout/', views.doLogout, name='logout'),
    path('home/blank/', views.blank),
    path('404/', views.load404, name='404'),
    path('home/index/', views.load_index, name='index'),
    path('adminHome/', views.loadAdmin, name='adminHome'),
    path('adminHome/addStu/', views.adminAddStu, name='adminAddStu'),
    path('adminHome/addStu/complete/', views.adminComStu, name='completeAddStu'),
    path('adminHome/addCourse/', views.adminAddCourse, name='addCourse'),
    path('adminHome/addCourse/complete/', views.adminComCourse, name='completeAddCourse'),
    path('adminHome/addStaff/', views.adminAddStaff, name='addStaff'),
    path('adminHome/addStaff/complete/', views.adminComStaff, name='completeAddStaff'),
    path('adminHome/manageCourse', views.adminMgrCourse, name='manageCourse'),
    path('adminHome/manageStu', views.adminMgrStu, name='manageStu'),
    path('staffHome/', views.staffHome, name='staffHome'),
]
