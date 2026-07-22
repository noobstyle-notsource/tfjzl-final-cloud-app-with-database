from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

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
            user = User.objects.create_user(
                username=username, 
                first_name=first_name, 
                last_name=last_name, 
                password=psw
            )
            login(request, user)
            return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/user_registration_bootstrap.html')

# Exam submission handlers
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user, 
        course=course
    )
    
    submission = Submission.objects.create(enrollment=enrollment)
    
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            choice_id = int(value)
            try:
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
            except Choice.DoesNotExist:
                pass
                
    submission.save()
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_ids = [choice.id for choice in submission.choices.all()]
    
    total_score = 0
    earned_score = 0
    
    # Query questions directly related to the course
    questions = Question.objects.filter(course=course)
    for question in questions:
        total_score += question.grade
        if question.is_get_score(selected_ids):
            earned_score += question.grade
                
    percentage = int((earned_score / total_score) * 100) if total_score > 0 else 0
    
    context['course'] = course
    context['grade'] = percentage
    context['total_score'] = total_score
    context['selected_ids'] = selected_ids
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        return redirect('onlinecourse:course_details', pk=course.id)
    return redirect('onlinecourse:index')