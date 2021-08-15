from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data = ((1, 'HOD'), (2, 'Staff'), (3, 'Student'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=255)


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class Staffs(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField(verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class Courses(models.Model):
    course_name = models.CharField(max_length=255, verbose_name='Название курса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class Subjects(models.Model):
    subject_name = models.CharField(max_length=255, verbose_name='Название предмета')
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255, verbose_name='Пол')
    profile_pic = models.FileField()
    address = models.TextField(verbose_name='Адрес')
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    session_start_year = models.DateField(default='2020-01-01', verbose_name='Год начала сессии')
    session_end_year = models.DateField(default='2023-01-01', verbose_name='Год окончания сессии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')


class Attendance(models.Model):
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата посещения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')


class AttendanceReport(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING, verbose_name='ID студента')
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE, verbose_name='ID посещаемости')
    status = models.BooleanField(default=False, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='ID студента')
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE, verbose_name='ID персонала')
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class FeedBackStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='ID студента')
    feedback = models.TextField(verbose_name='Обратная связь')
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class FeedBackStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE, verbose_name='ID персонала')
    feedback = models.TextField(verbose_name='Обратная связь')
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class NotificationStudents(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='ID студента')
    message = models.TextField(verbose_name='Уведомления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


class NotificationStaffs(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE, verbose_name='ID персонала')
    message = models.TextField(verbose_name='Уведомления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cоздано')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Oбновлено')
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
