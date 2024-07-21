from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=255)
    number_of_questions = models.IntegerField(default=0)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} by {self.host}"
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz,related_name="questions",on_delete=models.CASCADE)
    text = models.TextField()
    answer = models.TextField()
    question_no = models.IntegerField()
    def save(self, *args, **kwargs):
        if not self.question_no:
            self.question_no = self.quiz.questions.count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Q{self.question_no} of {self.quiz.title}"
        
    
