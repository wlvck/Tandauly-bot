from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from student_management_app.forms import AddStudentForm
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students
from django.shortcuts import get_object_or_404


def admin_page(request):
    return render(request, 'student_management_app/hod_template/home_content.html')


def add_staff(request):
    return render(request, 'student_management_app/hod_template/add_staff_template.html')


def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('Ket bar sagan kiruge bolmaid, tek kana Post methodtarga gana boladi')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                  email=email_address, password=password, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, 'Successfully Added Staff')
            return HttpResponseRedirect('add_staff')
        except ValueError:
            messages.error(request, 'Failed to Add Staff')
            return HttpResponseRedirect('add_staff')


def add_course(request):
    return render(request, 'student_management_app/hod_template/add_course_template.html')


def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse('Keteeeeeei na')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, 'Successfully Added Course')
            return HttpResponseRedirect('add_course')
        except ValueError:
            messages.error(request, 'Failed to Add Course')
            return HttpResponseRedirect('add_course')


def add_student(request):
    form = AddStudentForm()
    return render(request, 'student_management_app/hod_template/add_student_template.html',
                  {'form': form})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse('This method not allowed pawel nah')
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            session_start_year = form.cleaned_data['session_start']
            session_end_year = form.cleaned_data['session_end']
            course_id = form.cleaned_data['course']
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name,
                                                      last_name=last_name,
                                                      user_type=3, password=password)

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                user.students.session_start_year = session_start_year
                user.students.session_end_year = session_end_year
                user.students.gender = gender
                user.students.profile_pic = profile_pic_url
                user.students.address = address
                user.save()
                messages.success(request, 'Successfully Added Student')
                return HttpResponseRedirect('add_student')
            except ValueError:
                messages.error(request, 'Failed to Add Student')
                return HttpResponseRedirect('add_student')
        else:
            form = AddStudentForm()
            return render(request, 'student_management_app/hod_template/add_student_template.html',
                          {'form': form})


def add_subject(requet):
    staffs = CustomUser.objects.filter(user_type=2)
    courses = Courses.objects.all()
    return render(requet, 'student_management_app/hod_template/add_subject_template.html',
                  {'staffs': staffs, 'courses': courses})


def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse('Ketei na, sagan kiruge bolmaid')
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        course = Courses.objects.get(pk=course_id)
        staff_id = request.POST.get('staff_id')
        staff = CustomUser.objects.get(pk=staff_id)
        try:
            model = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            model.save()
            messages.success(request, 'Successfully Added Subject')
            return HttpResponseRedirect('add_subject')
        except ValueError:
            messages.error(request, 'Failed to Add Subject')
            return HttpResponseRedirect('add_subject')


def manage_staff(request):
    staff_data = Staffs.objects.all()
    return render(request, 'student_management_app/hod_template/manage_staff_template.html',
                  {'staff_data': staff_data})


def manage_student(request):
    students = Students.objects.all()
    return render(request, 'student_management_app/hod_template/manage_student_template.html',
                  {'students': students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'student_management_app/hod_template/manage_course_template.html',
                  {'courses': courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'student_management_app/hod_template/manage_subject_template.html',
                  {'subjects': subjects})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, 'student_management_app/hod_template/edit_staff_template.html',
                  {'staff': staff, 'id': staff_id})


def edit_staff_changes(request):
    if request.method != 'POST':
        return HttpResponse('Ketei na')
    else:
        staff_id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        email = request.POST.get('email_address')
        user = CustomUser.objects.get(id=staff_id)
        try:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            staff = Staffs.objects.get(admin=staff_id)
            staff.address = address
            staff.save()

            messages.success(request, 'You have successfully saved')
            return HttpResponseRedirect(f'edit_staff/{staff.admin.pk}')
        except ValueError:
            messages.error(request, 'Eptialmaid nestedin duris saktalmadigoi')
            return HttpResponseRedirect('edit_staff')


def edit_student(request, student_id):
    student = Students.objects.get(admin_id=student_id)
    courses = Courses.objects.all()
    return render(request, 'student_management_app/hod_template/edit_student_template.html', {'student': student,
                                                                                              'courses': courses,
                                                                                              'id': student_id})


def save_edited_student_changes(request):
    if request.method != 'POST':
        return HttpResponse('Ketei na')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        course = request.POST.get('course')
        gender = request.POST.get('gender')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        student_id = request.POST.get('student_id')
        user = CustomUser.objects.get(id=student_id)
        if request.FILES.get('profile_pic', False):
            profile_picture = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None
        try:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student_model = Students.objects.get(admin=student_id)
            student_model.address = address
            student_model.gender = gender
            student_model.session_start = session_start
            student_model.session_end = session_end
            student_model.profile_pic = profile_pic_url
            course_id = Courses.objects.get(id=course)
            student_model.course_id = course_id
            student_model.save()
            messages.success(request, 'AI jaraisin')
            return HttpResponseRedirect(f'edit_student/{student_id}')
        except ValueError:
            messages.error(request, 'ketei kate jberdin')
            return HttpResponseRedirect(f'edit_student/{student_id}')


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    teachers = Staffs.objects.all()
    return render(request, 'student_management_app/hod_template/edit_subject_template.html', {'subject': subject,
                                                                                              'courses': courses,
                                                                                              'teachers': teachers,
                                                                                              'id': subject_id})


def save_edited_subject_changes(request):
    if request.method != 'POST':
        return HttpResponse('Ketei na')
    else:
        subject_name = request.POST['subject_name']
        subject_id = request.POST['subject_id']
        course_name = request.POST['course_name']
        staff_name = request.POST['staff_name']

        subject = Subjects.objects.get(id=subject_id)
        course = Courses.objects.get(course_name=course_name)
        teacher = CustomUser.objects.get(first_name=staff_name)
        subject.subject_name = subject_name
        subject.course_id = course
        subject.staff_id = teacher
        subject.save()
        messages.success(request, 'Jaraisin')
        return HttpResponseRedirect('edit_subject/' + subject_id)


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, 'student_management_app/hod_template/edit_course_template.html', {'course': course,
                                                                                             'id': course_id})


def save_edited_course_changes(request):
    if request.method != 'POST':
        return HttpResponse('Ketei na')
    else:
        course_id = request.POST['course_id']
        course_name = request.POST['course_name']
        course = Courses.objects.get(id=course_id)
        try:
            course.course_name = course_name
            course.save()
            messages.success(request, 'Ai barekeldi')
            print(course_id)
            return HttpResponseRedirect('edit_course/' + course_id)
        except ValueError:
            messages.error(request, 'Ketei na')
            return HttpResponseRedirect('edit_course/' + course_id)
