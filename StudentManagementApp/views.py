from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def view_login(request):
    return render(request, 'login.html')


def view_register(request):
    return render(request, 'register.html')


def view_profile(request):
    return render(request, 'profile.html')


def doLogin(request):
    if request.method != 'POST':
        return HttpResponse('now allowed')
    return HttpResponse(request.POST['number'] + ' and ' + request.POST['password'])


def forgetPassword(request):
    return render(request, 'forgot-password.html')


def loadHome(request):
    return render(request, 'profile.html')


def loadTable(request):
    return render(request, 'table.html')
