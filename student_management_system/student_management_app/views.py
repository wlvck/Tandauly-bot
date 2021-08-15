from django.contrib import messages
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate

from student_management_app.EmailBackEnd import EmailBackEnd


def show_demo_page(requests):
    return render(requests, 'student_management_app/index.html')


def show_login_page(requests):
    return render(requests, 'student_management_app/login_page.html')


def dologin(requests):
    if requests.method != 'POST':
        return HttpResponse('<h1>Method Not Allowed For Get Method</h1>')
    else:
        user = EmailBackEnd.authenticate(requests, username=requests.POST['email'],
                                         password=requests.POST['password'])
        if user:
            login(requests, user)
            if user.user_type == '1':
                return HttpResponseRedirect('admin-page')
            elif user.user_type == '2':
                return HttpResponse('Staff 2')
            else:
                return HttpResponse('Student 3')
        else:
            messages.error(requests, 'Error')
            return HttpResponseRedirect('accaunts/login')


def get_user_details(requests):
    if requests.user:
        return HttpResponse('User:' + requests.user.email + '<br>' + 'User type: ' + str(requests.user.user_type))
    else:
        return HttpResponse('Please Login to access data')


def logout_user(requests):
    logout(requests)
    return HttpResponseRedirect('accaunts/login')
