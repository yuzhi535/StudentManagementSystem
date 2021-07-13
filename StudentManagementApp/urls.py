from django.conf.urls.static import static
from django.urls import path, include

from StudentManagementApp import views
from StudentManagementSystem import settings

urlpatterns = [
                  path('', views.view_login, name='login'),
                  path('register/', views.view_register),
                  path('doLogin/', views.doLogin, name='doLogin'),
                  path('forgot-password/<str:name>', views.resetPassword, name='resetPassword'),
                  path('resetPassword/reset/', views.reset, name='reset'),
                  path('home/', views.loadHome, name='home'),
                  path('home/table/<int:id>', views.loadTable, name='table'),
                  path('home/logout/', views.doLogout, name='logout'),
                  path('home/blank/', views.blank),
                  path('404/', views.load404, name='404'),
                  path('home/index/<int:id>', views.load_index, name='index'),
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
                  path('adminHome/addClass/', views.adminAddClass, name='adminAddClass'),
                  path('adminHome/addClass/complete', views.adminComClass, name='completeAddClass'),
                  path('adminHome/ManageStaff', views.adminMgrStaff, name='adminMgrStaff'),
                  path('adminHome/ManageStaff/manage/<int:pk>', views.AdminStaffMgrView, name='adminStaffMgr'),
                  path('adminHome/manageCourse/manage/<int:pk>', views.AdminCourseMgrView.as_view(),
                       name='adminCourseMgr'),
                  path('adminHome/manageClass/', views.adminClassMgr, name='adminMgrClass'),
                  path('adminHome/arrangeCourse/', views.adminArrangeCourse, name='adminArrangeCourse'),
                  path('adminHome/arrangeCourse/complete', views.adminComArrCourse, name='adminComArrCourse'),
                  path('adminHome/ManageStaff/manage/edit/<int:id>/', views.adminComMgrStaff,
                       name='adminComMgrStaffEdit'),
                  path('staffHome/aboutStu/<int:id>', views.staffAboutStu, name='staffAboutStu'),
                  path('staffHome/editStu/<int:id>', views.staffEditStu, name='staffEditStu'),
                  path('staffHome/about/<int:id>', views.staffAboutMe, name='staffAboutMe'),
                  path(
                      'staffHome/editStu/<int:id>/<int:id1>/<int:id2>/coursename=<str:coursename>/classname=<str'
                      ':classname>',
                      views.staffEditScore, name='staffEditScore'),
                  path('staffHome/edidStu/score/', views.staffEditStuScore, name='staffEditStuScore'),
                  path('adminHome/export_to_excel', views.stuExport, name='stuExport'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
