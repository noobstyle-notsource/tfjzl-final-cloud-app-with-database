from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission

# Course List View
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all()

# Course Detail View
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'

# Authentication Views
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        psw = request.POST['psw']
        user = authenticate(username=username, password=psw)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
    return redirect('onlinecourse:index')

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

def registration_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        psw = request.POST['psw']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            User.objects.get(username=username)
            return redirect('onlinecourse:index')
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=psw)
            login(request, user)
            return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/user_registration_bootstrap.html')

# Exam submission handlers (if defined/needed)
def submit(request, course_id):
    return redirect('onlinecourse:index')

def show_exam_result(request, course_id, submission_id):
    return render(request, 'onlinecourse/exam_result_bootstrap.html')

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        # Add enrollment logic here or redirect to course detail
        return redirect('onlinecourse:course_details', pk=course.id)
    return redirect('onlinecourse:index')