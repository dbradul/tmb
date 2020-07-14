
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, Count

from testsuite.models import TestResultDetail


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, blank=True)
    correct_answers = models.SmallIntegerField(default=0, null=True, blank=True)
    total_questions = models.SmallIntegerField(default=0, null=True, blank=True)

    def update_score(self):
        results = TestResultDetail.objects\
            .filter(
                test_result__user=self,
                test_result__is_completed=True)\
            .values(
                'test_result',
                'question')\
            .annotate(
                answers=Sum('is_correct'),
                questions=Count('question')
        )
        self.correct_answers = sum(result['answers'] == result['questions'] for result in results)
        self.total_questions = len(results)
        if self.total_questions:
            self.avr_score = self.correct_answers / self.total_questions * 100

    def points(self):
        return self.test_results.aggregate(total=Sum('avr_score')).get('total')

    def score_info(self):
        return f'{self.correct_answers} of {self.total_questions} ({self.avr_score:.2f}%)'