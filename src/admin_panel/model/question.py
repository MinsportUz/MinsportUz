from django.db import models
# from django.utils.translation import ugettext_lazy as _

from admin_panel.common import generate_field


class Quizz(models.Model):
    title = models.CharField(max_length=500)
    is_published = models.BooleanField(default=False)
    main_page = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quizz'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)

    @property
    def result_count(self):
        return QuestionResult.objects.filter(quizz=self).count()

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Quizz, self).save(*args, **kwargs)


class Question(models.Model):
    title = models.CharField(max_length=500)
    quizz = models.ForeignKey('Quizz', on_delete=models.CASCADE, related_name='question', null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'question'
        ordering = ['created_at']

    def __str__(self):
        return str(self.title)

    @property
    def percentage(self):
        if self.quizz and self.quizz.result_count > 0:
            overall = 100 / self.quizz.result_count
            obj = self.count * overall
            return int(obj)
        return 0

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Question, self).save(*args, **kwargs)


class QuestionResult(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='result')
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='result')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'question_result'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.quizz)
