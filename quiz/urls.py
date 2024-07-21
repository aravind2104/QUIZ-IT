from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.Home, name="home"),
    path("login/", views.LoginPage, name="login"),
    path("logout/",views.LogoutPage,name="logout"),
    path("register/",views.RegisterPage,name='register'),
    path("profile/",views.ProfilePage,name='profile'),
    path("create_quiz/",views.CreateQuiz,name='create-quiz'),
    path("add_question/<int:quiz_id>/",views.AddQuestion,name="add-question"),
    path("quiz-room/<int:quiz_id>/",views.QuizRoom,name="quiz-room"),
    path("attempt-quiz/<int:quiz_id>/",views.AttemptQuiz,name="attempt-quiz"),
    path("edit-question/<int:question_id>/",views.EditQuestion,name="edit-question"),
    path("delete-question/<int:question_id>/",views.DeleteQuestion,name="delete-question"),
    path("delete-quiz/<int:quiz_id>/",views.DeleteRoom,name="delete-quiz"),
]
