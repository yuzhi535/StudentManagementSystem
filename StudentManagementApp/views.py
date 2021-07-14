import csv
import datetime
import json
import re

import requests
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views import generic

# Create your views here.
from StudentManagementApp.UserBackEnd import UserBackEnd
from StudentManagementApp.models import CustomUser, Course, Study, StuClass, Staff, Student


def view_login(request):
    return render(request, 'login.html')


def view_register(request):
    return render(request, 'register.html')


def view_profile(request):
    return render(request, 'home.html')


def doLogin(request):
    if request.method != 'POST':
        return HttpResponse('now allowed')
    else:
        # 谷歌验证
        captcha_token = request.POST.get("g-recaptcha-response")
        # print(f'captcha_token = {captcha_token}')
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


def resetPassword(request, name):
    return render(request, 'forgot-password.html', {'name': name})


def loadHome(request):
    grade = int(timezone.now().year)
    convert = {1: '一', 2: '二', 3: '三', 4: '四'}
    return render(request, 'home.html', {'now': grade, 'convert': convert})


def loadTable(request, id):
    student = Student.objects.get(pk=id)
    studies = student.study_set.all()

    return render(request, 'table.html', {'studies': studies})


def doLogout(request):
    logout(request)
    return HttpResponseRedirect('/')


def blank(request):
    return render(request, 'base_template/base.html')


def load404(request):
    return render(request, '404.html')


def load_index(request, id):
    now = int(timezone.now().year)
    student = Student.objects.get(pk=id)
    scores = student.study_set.all()
    scores = [score.score for score in scores]
    score = sum(scores) // len(scores)
    id = student.id
    return render(request, 'index.html', {'now': now, 'score': score, 'id': id})


def loadAdmin(request):
    return render(request, 'adminHome.html')


def adminAddStu(request):
    choices = StuClass.objects.all()
    time = timezone.now()
    return render(request, 'adminAddStu.html', {'choices': choices, 'time': time})


def adminComStu(request):
    if request.method != 'POST':
        return HttpResponse('method is not allowed')
    else:
        user_id = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        passwd = request.POST.get('password')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        phone = request.POST.get('phone')
        time = request.POST.get('time')
        choice = request.POST.get('choice')
        dept = request.POST.get('dept')
        if dept == '':
            dept = '信工'
        pic_url = '#'
        if request.FILES.get('profile_pic'):
            pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(pic.name, pic)
            pic_url = fs.url(filename)

        try:
            if bool(re.search('[a-z]', user_id)):
                raise Exception
            if name == '' or email == '' or passwd == '' or address == '' or sex == '' or phone == '' or time == '' or choice == None or dept == '':
                raise Exception
            # 比较时间，不能是将来的时间
            time = parse_date(time)
            if datetime.datetime(time.year, time.month, time.day) > timezone.now():
                messages.error(request, '时间不能是未来!')
            elif len(CustomUser.objects.filter(user_id=user_id)) == 0:
                user = CustomUser.objects.create_user(user_id=user_id, username=name, email=email, password=passwd,
                                                      phone_number=phone, user_type=3, in_school_time=time
                                                      )
                user.student.address = address
                user.student.gender = sex
                user.student.inClass_id = choice
                user.student.pic = pic_url
                user.student.dept = dept
                user.save()
                messages.success(request, 'success!')
            else:
                messages.error(request, 'id重复了!')
        except:
            messages.error(request, '添加失败!提示：id是否是纯数字或者必填项未填')
        return HttpResponseRedirect('/adminHome/addStu/')


def adminAddCourse(request):
    return render(request, 'adminAddCourse.html')


def adminComCourse(request):
    if request.method != 'POST':
        return HttpResponse('method is not allowed')
    try:
        course_name = request.POST['course']
        credit = request.POST['credit']
        if course_name != '' and credit != '':
            model = Course.objects.create(name=course_name, credit=credit)
            model.save()
            messages.success(request, '添加课程成功')
            return HttpResponseRedirect(reverse('addCourse'))
        else:
            raise Exception
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
        dept = request.POST['dept']
        if dept == "":
            dept = '信工'

        pic_url = '/static/assets/img/avatars/zzu.png'
        if request.FILES.get('profile_pic'):
            pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(pic.name, pic)
            pic_url = fs.url(filename)

        try:
            if len(CustomUser.objects.filter(user_id=user_id)) == 0:
                user = CustomUser.objects.create_user(user_id=user_id, username=name, email=email, password=passwd,
                                                      phone_number=phone, user_type=2
                                                      )
                user.staff.address = address
                user.staff.gender = sex
                user.staff.pic = pic_url
                user.staff.dept = dept
                user.save()
                messages.success(request, 'success!')
            else:
                messages.error(request, 'failed!')
            return HttpResponseRedirect('/adminHome/addStaff/')
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

    id = request.POST.get('number')
    name = request.POST.get('name')
    subject = request.POST.get('subject')
    try:
        if id == '' or name == '' or subject == '':
            raise Exception

        model = StuClass.objects.create(class_id=id, name=name, subject=subject)
        model.save()

        messages.success(request, '添加班级成功')
    except Exception as e:
        messages.error(request, '添加班级失败, 请检查是否某些项未填')

    return HttpResponseRedirect(reverse('adminAddClass'))


def adminMgrStaff(request):
    content = Staff.objects.all()
    return render(request, 'adminMgrStaff.html', {'staffs': content})


# class AdminStaffMgrView(generic.ListView):
#     template_name = 'adminStaffMgr.html'
#     context_object_name = 'contents'
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         staff = Staff.objects.get(pk=pk)
#         return staff.teach_set.all(), staff.admin.username

def AdminStaffMgrView(request, pk):
    staff = Staff.objects.get(pk=pk)
    username = staff.admin.username
    courses = staff.courses.all()
    stuClass = StuClass.objects.all()

    return render(request, 'adminStaffMgr.html',
                  {'username': username, 'courses': courses, 'stuClass': stuClass, 'staff': staff})


class AdminCourseMgrView(generic.ListView):
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()


def reset(request):
    password = request.POST['password']
    confirm = request.POST['confirm']
    name = request.POST['username']
    if password != confirm:
        messages.error(request, '两次密码不符合')
        return HttpResponseRedirect(reverse('resetPassword', kwargs={'name': name}))
    elif password == '':
        messages.error(request, '请不要输入空密码')
        return HttpResponseRedirect(reverse('resetPassword', kwargs={'name': name}))
    else:
        user = CustomUser.objects.filter(username=name)[0]
        user.set_password(raw_password=password)
        user.save()
        return HttpResponseRedirect(reverse('login'))


def adminClassMgr(request):
    content = StuClass.objects.all()
    return render(request, 'adminMgrClass.html', {'content': content})


def adminArrangeCourse(request):
    courses = Course.objects.all()
    stuClass = StuClass.objects.all()
    staffs = Staff.objects.all()
    return render(request, 'adminArrangeCourse.html', {'courses': courses, 'classes': stuClass, 'staffs': staffs})


def adminComArrCourse(request):
    course_id = request.POST.get('course')
    class_id = request.POST.get('class')
    staff_id = request.POST.get('staff')
    try:
        if course_id == None or course_id == None or staff_id == None:
            raise Exception

        staff = Staff.objects.get(pk=staff_id)
        tclass = StuClass.objects.get(pk=class_id)
        course = Course.objects.get(pk=course_id)
        staff.courses.add(course)

        for student in tclass.student_set.all():
            study = Study.objects.create(score=-1)
            study.course = course
            study.student = student
            study.staff = staff
            study.save()

        staff.save()
        # tclass.save()

        messages.success(request, '安排课程成功')

    except Exception as e:
        messages.error(request, '安排课程失败')
    return HttpResponseRedirect(reverse('adminArrangeCourse'))


def adminComMgrStaff(request, id):
    class_id = request.POST['class']
    course_id = request.POST['course']
    staff = Staff.objects.get(pk=id)
    username = staff.admin.username
    try:
        course = Course.objects.get(pk=course_id)
        tclass = StuClass.objects.get(pk=class_id)
        study = course.study_set.filter(course=course)
        if len(study) == 0:
            messages.error(request, '删除失败')
        else:
            for s in study:
                s.delete()
                pass
            staff.courses.remove(course)
            course.staff_set.remove(staff)
            messages.success(request, '删除成功')
    except:
        messages.error(request, "删除失败")

    courses = Course.objects.all()
    stuClass = StuClass.objects.all()
    return render(request, 'adminStaffMgr.html',
                  {'username': username, 'courses': courses, 'stuClass': stuClass, 'staff': staff})


def staffAboutStu(request, id):
    staff = Staff.objects.get(pk=id)
    return render(request, 'staffAboutStu.html', {'staff': staff})


def staffEditStu(request, id):
    staff = Staff.objects.get(pk=id)
    return render(request, 'staffEditStu.html', {'staff': staff})


def staffAboutMe(request, id):
    staff = Staff.objects.get(pk=id)
    return render(request, 'staffAboutMe.html', {'staff': staff})


def staffEditScore(request, id, id1, id2, coursename, classname):
    staff = Staff.objects.get(pk=id2)
    student = Student.objects.get(pk=id)
    course = Course.objects.get(pk=id1)
    return render(request, 'staffEditStuScore.html',
                  {'staff': staff, 'student': student, 'course': id1, 'coursename': coursename, 'classname': classname})


def staffEditStuScore(request):
    score = request.POST['score']
    id = request.POST['id']
    id1 = request.POST['id1']
    id2 = request.POST['id2']
    coursename = request.POST['coursename']
    classname = request.POST['classname']
    if score == "":
        messages.error(request, '请输入成绩!')
        return HttpResponseRedirect(reverse(staffEditScore,
                                            kwargs={'id': id,
                                                    'id1': id1, 'id2': id2,
                                                    'coursename': coursename, 'classname': classname}))
    score = int(score)

    if score > 100 or score < 0:
        messages.error(request, '分数必须在0到100之间!')
        return HttpResponseRedirect(reverse(staffEditScore,
                                            kwargs={'id': id,
                                                    'id1': id1, 'id2': id2,
                                                    'coursename': coursename, 'classname': classname}))
    student = Student.objects.get(pk=id)
    course = Course.objects.get(pk=id1)
    studies = Study.objects.filter(student=student, course=course)
    for study in studies:
        study.score = score
        study.save()
        # study.score = F('score')
    return HttpResponseRedirect(reverse(staffAboutStu, kwargs={'id': id2}))


def stuExport(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['学生ID', '姓名', '邮箱', '手机号'])
    users = CustomUser.objects.values_list('user_id', 'username', 'email', 'phone_number')
    for user in users:
        writer.writerow(user)
    return response


def adminSearchStu(request):
    name = request.POST.get('search')
    if name == "*":
        content = Student.objects.all()
    else:
        # name = '%' + name + '%'
        contents = Student.objects.filter(admin__username__contains=name)
        content = [user for user in contents]
    return render(request, 'adminMgrStu.html', {'students': content, 'name': name})
