from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.settings import Typo
from django.views.generic import CreateView, UpdateView, ListView
from . import forms


# class TypoView(CreateView):
#     form_class = ErrorReportingForm
#
#     def get(self, request, *args, **kwargs):
#         return HttpResponseRedirect('/')
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'status': 'OK'})
#         else:
#             return JsonResponse({'status': 'Error'})


class TypoUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Typo
    form_class = forms.TypoForm
    context_object_name = 'object'
    template_name = 'back/typo/typo_update.html'
    success_url = reverse_lazy('typo:typo-list')

    def post(self, request, *args, **kwargs):
        typo = self.model.objects.get(id=self.kwargs['pk'])

        corrected = request.POST.get('corrected')

        if corrected == 'on':
            corrected = True
        else:
            corrected = False

        typo.corrected = corrected
        typo.save()
        return HttpResponseRedirect(self.success_url)


class TypoList(HasRoleMixin, ListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Typo
    template_name = 'back/typo/typo_list.html'
    queryset = model.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TypoList, self).get_context_data(object_list=object_list)
        objects = self.queryset

        q = self.request.GET.get('q')
        if q:
            objects = self.model.objects.filter(title__icontains=q)

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


class TypoDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = Typo
    success_url = reverse_lazy('typo:typo-list')
