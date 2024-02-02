from django.forms import ModelForm

from admin_panel.model import question


class QuizzForm(ModelForm):
    class Meta:
        model = question.Quizz
        fields = '__all__'


class QuestionForm(ModelForm):
    class Meta:
        model = question.Question
        fields = '__all__'

