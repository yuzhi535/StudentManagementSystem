from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from StudentManagementApp.UserBackEnd import UserBackEnd


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
    return render(request, 'base.html')


def load404(request):
    return render(request, '404.html')
