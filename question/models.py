from django.db import models
import uuid
from uuid import UUID

class Test(models.Model):
    ''' To Create a TEST/EXAM entry with marks, test title, duration, date, and description etc'''
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, db_index=True, primary_key=True
    )
    test_title = models.CharField(max_length=200)
    test_description = models.CharField(max_length=10000)
    sechduled_for = models.DateTimeField()
    total_marks = models.PositiveIntegerField()
    test_duration_minutes = models.PositiveIntegerField(help_text=_("Duration in minutes"))
    

class Question(models.Model): 
    ''' To Post questions with Test ID and quesiton string '''
    test = models.ForeignKey(Test, related_name='test', on_delete=models.CASCADE)
    question_text = models.TextField()
    
    class Meta :
      unique_together = [['test', 'question_text']]
      
    
class Choices(models.Model): 
    ''' To Create multiple choices for questions '''
    question = models.ForeignKey(Question, related_name='question', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default = False)
    
    class Meta :
      unique_together = [['question', 'choice_text']]
