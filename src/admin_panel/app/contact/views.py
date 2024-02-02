from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model import contact, ministry
from . import forms


class ContactList(HasRoleMixin, ListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Contact
    template_name = 'back/contact/contact_list.html'
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactList, self).get_context_data(object_list=object_list)
        objects = self.queryset

        q = self.request.GET.get('q')
        if q:
            objects = self.model.objects.filter(sender_name__icontains=q)
            if not objects:
                objects = self.model.objects.filter(id_number__icontains=q)

        page = self.request.GET.get('page', 1)
        paginator = Paginator(objects, 12)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['objects'] = objects

        return context


class ContactUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Contact
    template_name = 'back/contact/contact_update.html'
    form_class = forms.ContactForm
    success_url = reverse_lazy('contact:contact-list')

    def get(self, request, pk):
        context = {
            'contact': self.model.objects.get(id=self.kwargs['pk']),
            'status': contact.STATUS,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        contact = self.model.objects.get(id=self.kwargs['pk'])
        contact.status = self.request.POST.get('status')
        contact.save()
        return HttpResponseRedirect(self.success_url)


class ContactDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Contact
    success_url = reverse_lazy('contact:contact-list')


class FeedbackList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Feedback
    template_name = 'back/contact/feedback_list.html'
    queryset = model.objects.all().order_by('-created_at')


class FeedbackUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Feedback
    template_name = 'back/contact/feedback_update.html'
    form_class = forms.FeedbackForm
    success_url = reverse_lazy('contact:feedback-list')

    def get(self, request, pk):
        context = {
            'contact': self.model.objects.get(id=self.kwargs['pk']),
            'status': contact.STATUS,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        contact = self.model.objects.get(id=self.kwargs['pk'])
        contact.status = self.request.POST.get('status')
        contact.save()
        return HttpResponseRedirect(self.success_url)


class FeedbackDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Feedback
    success_url = reverse_lazy('contact:feedback-list')


# RECEPTION

class ReceptionCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Reception
    template_name = 'back/contact/reception_create.html'
    form_class = forms.ReceptionForm
    success_url = reverse_lazy('contact:reception-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceptionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context['staff'] = ministry.Staff.objects.filter(leader=True)
        context['day'] = contact.WeekDay.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('active') == 'on':
            data['active'] = True
        else:
            data['active'] = False

        if data.get('staff'):
            data['staff'] = ministry.Staff.objects.get(id=int(data['staff']))

        if data.get('day'):
            data['day'] = contact.WeekDay.objects.get(id=int(data['day']))

        obj = self.model(**data)
        obj.save()

        return HttpResponseRedirect(self.success_url)


class ReceptionUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Reception
    template_name = 'back/contact/reception_update.html'
    context_object_name = 'object'
    form_class = forms.ReceptionForm
    success_url = reverse_lazy('contact:reception-list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReceptionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context['staff'] = ministry.Staff.objects.filter(leader=True)
        context['day'] = contact.WeekDay.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        obj = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('staff'):
            data['staff'] = ministry.Staff.objects.get(id=int(data['staff']))

        if data.get('day'):
            data['day'] = contact.WeekDay.objects.get(id=int(data['day']))

        if data.get('active') == 'on':
            data['active'] = True
        else:
            data['active'] = False

        obj.staff = data['staff']
        obj.day = data['day']
        obj.active = data['active']
        obj.time = data['time']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ReceptionList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Reception
    template_name = 'back/contact/reception_list.html'
    queryset = model.objects.all()


class ReceptionDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = contact.Reception
    success_url = reverse_lazy('contact:reception-list')
