from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Quiz, QuizResult, CustomUser
from .serializers import CustomUserSerializer
from .forms import QuizForm, CustomUserCreationForm, LoginForm

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

def quiz_list(request):
    return render(request, 'quiz_app/quiz_list.html')

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    return render(request, 'quiz_app/quiz_detail.html', {'quiz': quiz, 'questions': questions})

def buttonclick1(request):
    return redirect('quiz_app/register.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'quiz_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('buttonclick')  
    else:
        form = LoginForm()
    return render(request, 'quiz_app/login.html', {'form': form})

@login_required
def buttonclick(request):
    user = request.user
    username = request.user.username
    quizzes = Quiz.objects.all()
    box = {
        'user': user,
        'quizzes': quizzes,
        'username': username,
    }
    return render(request, 'quiz_app/quiz_enter.html', box)

@login_required
def quiz_view(request, quiz_id):
    correct_count = 0
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, quiz_id=quiz.id)
        if form.is_valid():
            selected_answers = {key: form.cleaned_data[key] for key in form.cleaned_data}
            results = {}
            for question_id, answer in selected_answers.items():
                is_correct = answer.is_correct
                if answer.is_correct:
                    correct_count += 1
                results[question_id] = {
                    'answer': answer,
                    'is_correct': is_correct,
                }
            QuizResult.objects.create(User=request.user, Quiz=quiz, correct_answers_count=correct_count)
            context = {
                'selected_answers': selected_answers,
                'results': results,
                'QuizResult.objects.create': QuizResult.objects.create,
            }
            return render(request, 'quiz_app/quiz_result.html', context)
    else:
        form = QuizForm()

    return render(request, 'quiz_app/quiz.html', {'form': form})

@login_required
def test_results(request):
    results = QuizResult.objects.filter(User=request.user)
    return render(request, 'quiz_app/test_results.html', {'results': results})