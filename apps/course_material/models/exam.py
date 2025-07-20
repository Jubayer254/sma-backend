from django.db import models
from course_material.models.base_model import BaseModel
from course_material.models.course import Batch

class Exam(BaseModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveBigIntegerField(help_text="Duration in minutes")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.batch} - {self.title}"

    class Meta:
        db_table = 'exams'
        ordering = ['start_datetime']
        verbose_name = "6. Exam"
        verbose_name_plural = "6. Exams"


class Question(BaseModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.exam.title}"

    class Meta:
        db_table = 'questions'
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.answer_text[:50]}"

    class Meta:
        db_table = 'answers'