import datetime
import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import requests

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views import generic
from django.views.generic import ListView

from StudentManagementApp.UserBackEnd import UserBackEnd
from StudentManagementApp.models import CustomUser, Course, Study, StuClass, Staff, Teach, Student


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
        # 谷歌验证
        captcha_token = request.POST.get("g-recaptcha-response")
        print(f'captcha_token = {captcha_token}')
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = '6LeH_40bAAAAAODsq20WVtf2veH8agognlCcjAY1'
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success'] == False:
            messages.error(request, '请证明您是人类')
            return HttpResponseRedirect("/")

        user = UserBackEnd.authenticate(request, request.POST['number'], request.POST['password'])
        if user is not None:
            login(request, user)
            # 注意是字符串
            if user.user_type == '1':
                return HttpResponseRedirect(reverse('adminHome'))
            elif user.user_type == '2':
                return HttpResponseRedirect(reverse('staffHome'))
            elif user.user_type == '3':
                return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, '无效用户名或密码')
            return HttpResponseRedirect("/")


def resetPassword(request):
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
    choices = StuClass.objects.all()
    return render(request, 'adminAddStu.html', {'choices': choices})


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
        time = request.POST['time']
        time = parse_date(time)
        choice = request.POST['choice']

        try:
            # 比较时间，不能是将来的时间
            if datetime.datetime(time.year, time.month, time.day) > timezone.now():
                messages.error(request, 'failed!')
            elif len(CustomUser.objects.filter(user_id=user_id)) == 0:
                user = CustomUser.objects.create_user(user_id=user_id, username=name, email=email, password=passwd,
                                                      phone_number=phone, user_type=3, in_school_time=time
                                                      )
                user.student.address = address
                user.student.gender = sex
                user.student.inClass_id = int(choice)
                user.save()
                messages.success(request, 'success!')
            else:
                messages.error(request, 'failed!')
        except:
            messages.error(request, 'failed!')
    return HttpResponseRedirect('/adminHome/addStu/')


def adminAddCourse(request):
    return render(request, 'adminAddCourse.html')


def adminComCourse(request):
    if request.method != 'POST':
        return HttpResponse('method is not allowed')
    try:
        course_name = request.POST['course']
        credit = request.POST['credit']
        model = Course.objects.create(name=course_name, credit=credit)
        model.save()
        messages.success(request, '添加课程成功')
        return HttpResponseRedirect(reverse('addCourse'))

    except:
        messages.error(request, '添加课程失败')
        return HttpResponseRedirect(reverse('addCourse'))


def adminAddStaff(request):
    return render(request, 'adminAddStaff.html')


def adminComStaff(request):
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
            if len(CustomUser.objects.filter(user_id=user_id)) == 0:
                user = CustomUser.objects.create_user(user_id=user_id, username=name, email=email, password=passwd,
                                                      phone_number=phone, user_type=2
                                                      )
                user.staff.address = address
                user.staff.gender = sex
                user.save()
                messages.success(request, 'success!')
            else:
                messages.error(request, 'failed!')
            return HttpResponseRedirect(reverse('adminAddStaff'))
        except:
            messages.error(request, 'failed!')
            return HttpResponseRedirect('/adminHome/addStaff/')


def adminMgrCourse(request):
    content = Course.objects.all()
    return render(request, 'adminMgrCourse.html', {'courses': content})


def adminMgrStu(request):
    content = Student.objects.all()
    return render(request, 'adminMgrStu.html', {'students': content})


def staffHome(request):
    return render(request, 'staffHome.html')


def adminAddClass(request):
    # content = StuClass.objects.all()
    return render(request, 'adminAddClass.html')


def adminComClass(request):
    if request.method != 'POST':
        return HttpResponse('method is not allowed')

    id = request.POST['number']
    name = request.POST['name']
    try:
        model = StuClass.objects.create(class_id=id, name=name)
        model.save()

        messages.success(request, '添加班级成功')
    except Exception as e:
        messages.error(request, '添加班级失败')

    return HttpResponseRedirect(reverse('adminAddClass'))


# todo 教务处管理界面上，管理教员页面即罗列教员，其中可点击到某个具体教员身上，然后对他安排到教某个班某个课程
# todo 重设密码
# todo 教务处页面罗列班级、教员、学生

def adminMgrStaff(request):
    content = Staff.objects.all()
    return render(request, 'adminMgrStaff.html', {'staffs': content})


class AdminStaffMgrView(generic.ListView):
    template_name = 'adminStaffMgr.html'
    context_object_name = 'contents'

    def get_queryset(self):
        pk = self.kwargs['pk']
        staff = Staff.objects.get(pk=pk)
        return staff.teach_set.all(), staff.admin.username


class AdminCourseMgrView(generic.ListView):
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()
