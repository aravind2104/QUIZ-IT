from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .forms import UserRegisterForm,UserLoginForm,QuestionForm,QuizForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Quiz, Question
from django.core.paginator import Paginator

# Create your views here.
def Home(request):
    quizzes=Quiz.objects.all()
    context={'quizzes':quizzes}
    return render(request, 'home.html',context)

def LoginPage(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def RegisterPage(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def LogoutPage(request):
    logout(request)
    return redirect('home')

def ProfilePage(request):
    quizzes=Quiz.objects.filter(host=request.user)
    context={'quizzes':quizzes}
    return render(request, "profile.html",context)

@login_required
def CreateQuiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.host = request.user
            quiz.save()
            return redirect('add-question',quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'create_quiz.html', {'form': form})

@login_required
def AddQuestion(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            quiz.number_of_questions=quiz.questions.count()
            quiz.save()
            return redirect('quiz-room',quiz_id=quiz.id)
    else:
        form = QuestionForm(initial={'quiz': quiz})
    return render(request, 'add_question.html', {'form': form})

@login_required
def QuizRoom(request,quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    return render(request, 'quiz_room.html', {'quiz': quiz, 'questions': questions})

@login_required
def AttemptQuiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()
    paginator = Paginator(questions, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'quiz':quiz , 'page_obj':page_obj}
    if request.method == 'POST':
        user_answers = request.session.get('user_answers', {})
        user_answer = request.POST.get(f'answer_{page_obj.object_list[0].id}')
        if user_answer:
            user_answers[str(page_obj.object_list[0].id)] = user_answer
            request.session['user_answers'] = user_answers
        if page_obj.has_next():
            return redirect(f'{reverse("attempt-quiz", kwargs={"quiz_id": quiz_id})}?page={page_obj.next_page_number()}')
        else:
            correct_answers = 0
            detailed_results = []
            for question in questions:
                user_answer = user_answers.get(str(question.id), "")
                is_correct = user_answer.strip().lower() == question.answer.strip().lower()
                if is_correct:
                    correct_answers += 1
                detailed_results.append({'question': question,'user_answer': user_answer,'is_correct': is_correct})
            score = correct_answers
            request.session.pop('user_answers', None) 
            context={'quiz':quiz , 'detailed_results':detailed_results, 'correct_answers':correct_answers, 'total_questions':questions.count(), 'score':score}
            return render(request, 'result.html', context)
    return render(request, 'attempt_quiz.html', context)

def EditQuestion(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('quiz-room', quiz_id=question.quiz.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form, 'question': question}
    return render(request, 'edit_question.html', context)

def DeleteQuestion(request, question_id):
    question = Question.objects.get(id=question_id)
    quiz = question.quiz
    if request.method == 'POST':
        question_no_to_delete = question.question_no
        question.delete()
        remaining_questions = quiz.questions.filter(question_no__gt=question_no_to_delete).order_by('question_no')
        for q in remaining_questions:
            q.question_no -= 1
            q.save()
        quiz.number_of_questions = quiz.questions.count()
        quiz.save()
        return redirect('quiz-room', quiz_id=quiz.id)
    context = {'question': question}
    return render(request, 'confirm_delete.html', context)

def DeleteRoom(request,quiz_id):
    quiz=Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('profile')
    context={'quiz':quiz}
    return render(request, 'delete_room.html', context)