from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from . import forms
from admin_panel.model.press_service import PhotoGallery, PhotoGalleryImage, VideoGallery
from admin_panel.app import views as custom


class PhotoCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = PhotoGallery
    form_class = forms.PhotoForm
    template_name = 'back/press_service/photo_gallery_create.html'
    success_url = reverse_lazy('gallery:photo-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['publish_date']:
            del data['publish_date']

        obj = self.model(**data)

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            obj.thumbnail = thumbnail

        obj.save()

        images = request.FILES.getlist('image')
        if images:
            for image in images:
                PhotoGalleryImage.objects.create(photo_gallery=obj, image=image)

        # obj.save()
        return HttpResponseRedirect(self.success_url)


class PhotoList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = PhotoGallery
    form_class = forms.PhotoForm
    queryset = model.objects.all()
    template_name = 'back/press_service/photo_gallery_list.html'


class PhotoUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = PhotoGallery
    form_class = forms.PhotoForm
    context_object_name = 'object'
    template_name = 'back/press_service/photo_gallery_update.html'
    success_url = reverse_lazy('gallery:photo-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        obj = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['publish_date']:
            del data['publish_date']

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            obj.thumbnail = thumbnail

        images = request.FILES.getlist('image')

        if images:
            for image in images:
                image, _ = PhotoGalleryImage.objects.get_or_create(photo_gallery=obj, image=image)

        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')
        obj.publish_date = data.get('publish_date')
        obj.is_published = data.get('is_published')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class PhotoDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = PhotoGallery
    success_url = reverse_lazy('gallery:photo-list')


# VIDEOGALLAERY VIEWS

class VideoCreate(HasRoleMixin, CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = VideoGallery
    form_class = forms.VideoForm
    template_name = 'back/press_service/video_gallery_create.html'
    success_url = reverse_lazy('gallery:video-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['publish_date']:
            del data['publish_date']

        video_gallery = self.model(**data)

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            video_gallery.thumbnail = thumbnail

        video_gallery.save()
        return HttpResponseRedirect(self.success_url)


class VideoList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = VideoGallery
    queryset = model.objects.all()
    template_name = 'back/press_service/video_gallery_list.html'


class VideoUpdate(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = VideoGallery
    form_class = forms.VideoForm
    context_object_name = 'object'
    template_name = 'back/press_service/video_gallery_update.html'
    success_url = reverse_lazy('gallery:video-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        obj = self.model.objects.get(id=self.kwargs['pk'])

        if data.get('is_published') == 'on':
            data['is_published'] = True
        else:
            data['is_published'] = False

        if not data['publish_date']:
            del data['publish_date']

        thumbnail = request.FILES.get('thumbnail')

        if thumbnail:
            obj.thumbnail = thumbnail

        obj.video_link = data.get('video_link')
        obj.title_uz = data.get('title_uz')
        obj.title_ru = data.get('title_ru')
        obj.title_en = data.get('title_en')

        obj.description_uz = data.get('description_uz')
        obj.description_ru = data.get('description_ru')
        obj.description_en = data.get('description_en')
        obj.is_published = data.get('is_published')
        obj.publish_date = data.get('publish_date')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class VideoDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = VideoGallery
    success_url = reverse_lazy('gallery:video-list')
