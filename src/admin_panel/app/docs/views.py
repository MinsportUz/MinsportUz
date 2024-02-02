from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.docs import Docs, DocType
from . import forms


# DOCUMENTS
class DocsCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Docs
    form_class = forms.DocsForm
    template_name = 'back/docs/doc_create.html'
    success_url = reverse_lazy('docs:docs-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocsCreate, self).get_context_data(object_list=object_list, **kwargs)
        doc_types = DocType.objects.all()
        context['doc_types'] = doc_types
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['date']:
            del data['date']

        if data.get('doc_type'):
            doc_type = DocType.objects.get(id=int(data['doc_type']))
            del data['doc_type']
            docs = self.model.objects.create(doc_type=doc_type, **data)
        else:
            docs = self.model.objects.create(**data)

        file = request.FILES.get('file')
        if file:
            docs.file = file

        docs.save()
        return HttpResponseRedirect(self.success_url)


class DocsUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Docs
    form_class = forms.DocsForm
    context_object_name = 'docs'
    template_name = 'back/docs/doc_update.html'
    success_url = reverse_lazy('docs:docs-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        doc_types = DocType.objects.all()
        context['doc_types'] = doc_types
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        docs = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['date']:
            del data['date']

        if 'doc_type' in data:
            docs.doc_type = DocType.objects.get(id=int(data['doc_type']))

        docs.title_uz = data.get('title_uz')
        docs.title_ru = data.get('title_ru')
        docs.title_en = data.get('title_en')

        docs.issued_by_uz = data.get('issued_by_uz')
        docs.issued_by_ru = data.get('issued_by_ru')
        docs.issued_by_en = data.get('issued_by_en')

        docs.law_uz = data.get('law_uz')
        docs.law_ru = data.get('law_ru')
        docs.law_en = data.get('law_en')

        docs.is_published = data.get('is_published')
        docs.date = data.get('date')
        docs.url = data.get('url')

        file = request.FILES.get('file')
        if file:
            docs.file = file

        docs.save()
        return HttpResponseRedirect(self.success_url)


class DocsList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Docs
    template_name = 'back/docs/doc_list.html'
    queryset = model.objects.all()


class DocsDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Docs
    success_url = reverse_lazy('docs:docs-list')


# DOCUMENT TYPES
class DocTypeCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = DocType
    form_class = forms.DocTypeForm
    template_name = 'back/docs/doc_type_create.html'
    success_url = reverse_lazy('docs:doc-type-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        doc_type = self.model(**data)
        doc_type.save()
        return HttpResponseRedirect(self.success_url)


class DocTypeUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = DocType
    form_class = forms.DocTypeForm
    context_object_name = 'doc_type'
    template_name = 'back/docs/doc_type_update.html'
    success_url = reverse_lazy('docs:doc-type-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        doc_type = self.model.objects.get(id=self.kwargs['pk'])

        doc_type.title_uz = data.get('title_uz')
        doc_type.title_ru = data.get('title_ru')
        doc_type.title_en = data.get('title_en')
        doc_type.order = data.get('order')
        doc_type.link = data.get('link')

        doc_type.save()
        return HttpResponseRedirect(self.success_url)


class DocTypeList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = DocType
    template_name = 'back/docs/doc_type_list.html'
    queryset = DocType.objects.all()


class DocTypeDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = DocType
    success_url = reverse_lazy('docs:docs-list')
