from django.core import paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from admin_panel.model.ministry import Staff
from admin_panel.model.territorial import Region, District


class CustomCreateView(CreateView):
    model = None
    form_class = None
    template_name = None
    success_url = None

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(self.model, self).get_context_data(object_list=object_list, **kwargs)
    #     return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        print(data, 1231)

        if data.get('region'):
            data['region'] = Region.objects.get(id=int(data['region']))

        if data.get('district'):
            data['district'] = District.objects.get(id=int(data['district']))

        obj = self.model(**data)
        obj.save()

        image = request.FILES.get('image')
        if image:
            obj.image = image

        obj.save()

        return HttpResponseRedirect(self.success_url)


class CustomUpdateView(UpdateView):
    model = None
    form_class = None
    context_object_name = None
    template_name = None
    success_url = None

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        obj = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('region'):
            data['region'] = Region.objects.get(id=int(data['region']))

        if data.get('district'):
            data['district'] = District.objects.get(id=int(data['district']))

        obj.title_uz = data['title_uz']
        obj.title_ru = data['title_ru']
        obj.title_en = data['title_en']

        # obj.address_uz = data['address_uz']
        # obj.address_ru = data['address_ru']
        # obj.address_en = data['address_en']

        # obj.instagram = data['instagram']
        # obj.facebook = data['facebook']
        # obj.telegram = data['telegram']
        # obj.twitter = data['twitter']

        # obj.email = data['email']
        # obj.phone_number = data['phone_number']
        obj.region = data['region']
        obj.district = data['district']
        # obj.lat = data['lat']
        # obj.long = data['long']
        # obj.link = data['link']

        if request.FILES.get('image'):
            obj.image = request.FILES.get('image')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class CustomListView(ListView):
    model = None
    template_name = None
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomListView, self).get_context_data(object_list=object_list)
        objects = self.queryset

        q = self.request.GET.get('q')
        if q:
            if self.request.LANGUAGE_CODE == 'en':
                objects = self.model.objects.filter(title_en__icontains=q)
            if self.request.LANGUAGE_CODE == 'ru':
                objects = self.model.objects.filter(title_ru__icontains=q)
            if self.request.LANGUAGE_CODE == 'uz':
                objects = self.model.objects.filter(title_uz__icontains=q)

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


class CustomDeleteView(DeleteView):
    model = None
    success_url = None

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        return HttpResponseRedirect(self.success_url)
