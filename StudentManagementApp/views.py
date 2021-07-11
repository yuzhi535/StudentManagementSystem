from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from StudentManagementApp.UserBackEnd import UserBackEnd
from StudentManagementApp.models import CustomUser


def view_login(request):
    return render(request, 'login.html')


def view_register(request):
    return render(request, 'register.html')


def view_profile(request):
    return render(request, 'profile.html')


def doLogin(request):
    if request.method != 'POST':
        return HttpResponse('now allowed')
    else:
        user = UserBackEnd.authenticate(request, request.POST['number'], request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            messages.error(request, '无效用户名或密码')
            return HttpResponseRedirect("/")


def forgetPassword(request):
    return render(request, 'forgot-password.html')


def loadHome(request):
    return render(request, 'profile.html')


def loadTable(request):
    return render(request, 'table.html')


def doLogout(request):
    logout(request)
    return HttpResponseRedirect('/')


def blank(request):
    return render(request, 'base_template/base.html')


def load404(request):
    return render(request, '404.html')


def load_index(request):
    return render(request, 'index.html')


def loadAdmin(request):
    return render(request, 'adminHome.html')


def adminAddStu(request):
    return render(request, 'adminAddStu.html')


def adminComStu(request):
    if request.method != 'POST':
        return HttpResponse('method is not allowed')
    else:
        user_id = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        passwd = request.POST['password']
        address = request.POST['address']
        sex = request.POST['sex']
        phone = request.POST['phone']
        try:
            if (CustomUser.objects.filter(user_id=user_id) == None):
                user = CustomUser.objects.create_user(user_id=user_id, username=name, email=email, password=passwd,
                                                      phone_number=phone, user_type=3
                                                      )
                user.student.address = address
                user.student.gender = sex
                # user.student.address = address
                user.save()
                messages.success(request, 'success!')
            else:
                messages.error(request, 'failed!')
            return HttpResponseRedirect(reverse('adminAddStu'))
        except:
            messages.error(request, 'failed!')
            return HttpResponseRedirect('/adminHome/addStu/')


def adminAddCourse(request):
    return render(request, 'adminAddCourse.html')


def adminAddStaff(request):
    return render(request, 'adminAddStaff.html')
