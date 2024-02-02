from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.mixins import HasRoleMixin
from django.utils.translation import gettext as _

from admin_panel.app import views as custom
from admin_panel.model import question
from . import forms, serializers


def BoolCheck(value):
    return True if value == 'on' else False


class QuizzCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = question.Quizz
    form_class = forms.QuizzForm
    template_name = 'back/quizz/quizz_create.html'
    # temporary for creating
    success_url = reverse_lazy('quizz:quizz-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuizzCreate, self).get_context_data(object_list=object_list)
        lang = self.request.LANGUAGE_CODE
        api_url = '/panel/quizz/api/'
        host = self.request.build_absolute_uri('/')[:-1]
        api = "%s/%s%screate/" % (host, lang, api_url)
        post = "%s/%s%screate/" % (host, lang, api_url)
        delete = "%s/%s%sdelete/" % (host, lang, api_url)
        context['api'] = api
        context['post'] = post
        context['delete'] = delete

        return context


class QuizzCreateAPI(HasRoleMixin, APIView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    success_url = reverse_lazy('quizz:quizz-list')

    def post(self, request, *args, **kwargs):
        data = request.data.get('payload')
        quizz_data = data['quizz']


        try:
            quizz = question.Quizz.objects.create(**quizz_data)
            # FOR TEST (Template will have its own checkbox)
            quizz.save()

            answers = data['question']
            for answer in answers:
                del answer['id']
                obj = question.Question.objects.create(**answer)
                obj.quizz = quizz
                obj.save()
            return Response(_("Muvaffaqiyatli saqlandi"), status=201)
        except Exception:
            return Response(_("Xatolik yuz berdi"), status=200)



class QuizzUpdateAPI(HasRoleMixin, APIView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'

    def get_object(self, query, pk):
        try:
            return query.objects.get(id=pk)
        except query.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        obj = self.get_object(question.Quizz, pk)

        answers = question.Question.objects.filter(quizz=obj)
        serializer = serializers.QuestionSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request, pk, *args, **kwargs):
        data = request.data.get('payload')
        quizz_data = data['quizz']
        answers = data['question']
        try:
            obj = self.get_object(question.Quizz, pk)

            obj.title_uz = quizz_data['title_uz']
            obj.title_ru = quizz_data['title_ru']
            obj.title_en = quizz_data['title_en']
            obj.main_page = quizz_data['main_page']
            obj.is_published = quizz_data['is_published']
            obj.save()

            for answer in answers:
                child = question.Question.objects.filter(id=int(answer['id']))
                if child.exists():
                    child = child.last()
                    child.title_uz = answer['title_uz']
                    child.title_ru = answer['title_ru']
                    child.title_en = answer['title_en']
                    child.quizz = obj
                    child.save()
                else:
                    del answer['id']
                    child = question.Question.objects.create(title_uz=answer['title_uz'],
                                                             title_ru=answer['title_ru'],
                                                             title_en=answer['title_en'],
                                                             quizz=obj
                                                             )
            return Response(_("Muvaffaqiyatli saqlandi"), status=201)
        except Exception:
            return Response(_("Xatolik yuz berdi"), status=200)




class QuestionDelete(HasRoleMixin, APIView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'

    def post(self, request, *args, **kwargs):
        instance = question.Question.objects.filter(id=request.data.get('id'))
        if instance.exists():
            instance.last().delete()
            return Response('Deleted', status=status.HTTP_204_NO_CONTENT)
        return Response('Not Deleted', status=status.HTTP_204_NO_CONTENT)


class QuizzUpdate(HasRoleMixin, custom.UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = question.Quizz
    form_class = forms.QuizzForm
    template_name = 'back/quizz/quizz_update.html'
    context_object_name = 'object'
    # temporary for creating
    success_url = reverse_lazy('quizz:quizz-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuizzUpdate, self).get_context_data(object_list=object_list)
        lang = self.request.LANGUAGE_CODE
        api_url = '/panel/quizz/api/'
        host = self.request.build_absolute_uri('/')[:-1]
        api = "%s/%s%s" % (host, lang, api_url)
        post = "%s/%s%screate/" % (host, lang, api_url)
        delete = "%s/%s%sdelete/" % (host, lang, api_url)
        context['api'] = api
        context['post'] = post
        context['delete'] = delete

        return context


class QuizzList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = question.Quizz
    template_name = 'back/quizz/quizz_list.html'
    queryset = model.objects.all()


class QuizzDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = question.Quizz
    success_url = reverse_lazy('quizz:quizz-list')
