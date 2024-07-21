from django import forms
from .models import Quiz,Question
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description','category']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'text','answer']
        