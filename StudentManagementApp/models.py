from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=255, verbose_name='用户ID')
    phone_number = models.IntegerField(verbose_name='手机号')
    in_school_time = models.DateTimeField(auto_now_add=True)
    user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    REQUIRED_FIELDS = ['user_id', 'phone_number', 'email']


# Create your models here.
class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=255, verbose_name='学号')
    # name = models.CharField(max_length=255, help_text='姓名', verbose_name='学生姓名')
    gender = models.CharField(max_length=4, choices=[('男', '男性'), ('女', '女性')], help_text='性别')
    # email = models.EmailField()
    # passwd = models.CharField(max_length=255)
    address = models.TextField()

    pic = models.FileField(verbose_name='个人照片')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'

    def __str__(self):
        return self.admin.username


class Staff(models.Model):
    id = models.CharField(primary_key=True, max_length=255, verbose_name='教师号')
    # name = models.CharField(max_length=255, help_text='姓名', verbose_name='学生姓名')
    gender = models.CharField(max_length=4, choices=[('男', '男性'), ('女', '女性')], help_text='性别')
    # email = models.EmailField()
    # passwd = models.CharField(max_length=255)
    address = models.TextField()
    # phone_number = models.IntegerField(verbose_name='手机号')
    pic = models.FileField(verbose_name='个人照片')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '教员'
        verbose_name_plural = '教员'


class Admin(models.Model):
    id = models.CharField(primary_key=True, max_length=255, verbose_name='学号')
    # name = models.CharField(max_length=255, help_text='姓名', verbose_name='学生姓名')
    gender = models.CharField(max_length=4, choices=[('男', '男性'), ('女', '女性')], help_text='性别')
    # email = models.EmailField()
    # passwd = models.CharField(max_length=255)
    address = models.TextField()
    # phone_number = models.IntegerField(verbose_name='手机号', default=1)
    pic = models.FileField(verbose_name='个人照片')
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '教务处'
        verbose_name_plural = '教务处'


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='课程名称')
    credit = models.IntegerField(verbose_name='学分')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = "课程"


class Study(models.Model):
    stu_id = models.ManyToManyField(Student)
    course_id = models.ManyToManyField(Course)
    score = models.IntegerField()

    class Meta:
        verbose_name = '修习'
        verbose_name_plural = '修习'


class Teach(models.Model):
    stu_id = models.ManyToManyField(Student)
    staff_id = models.ManyToManyField(Staff)

    class Meta:
        verbose_name = '教学'
        verbose_name_plural = '教学'


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance, id=instance.user_id)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance, id=instance.user_id)
        if instance.user_type == 3:
            Student.objects.create(admin=instance, id=instance.user_id)


@receiver(post_save, sender=CustomUser)
def save_suer_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.id = instance.admin.admin_id
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.id = instance.staff.admin_id
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.id = instance.student.admin_id
        instance.student.save()
