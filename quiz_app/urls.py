from django.urls import path
from . import views
from .views import buttonclick, buttonclick1, quiz_view, register, login_view, test_results


urlpatterns = [
    path('', views.quiz_list, name='home'),
    path('quiz/', buttonclick, name='buttonclick'),
    path('redirect/', buttonclick1, name='buttonclick1'),
    path('quiz/<int:quiz_id>/', quiz_view, name='quiz'),
    path('quiz/result/', test_results, name='result'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]