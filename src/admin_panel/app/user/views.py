from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rolepermissions.mixins import HasRoleMixin

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import CreateCustomUserForm
from django.contrib import messages
from django.views import generic
from admin_panel.app import views as custom
from admin_panel.model.user import CustomUser
from ...model.territorial import Region
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


class CreateCustomUserView(HasRoleMixin, generic.CreateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = CustomUser
    template_name = 'back/user/user_create.html'
    form_class = CreateCustomUserForm
    success_url = reverse_lazy('user:user-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        username = data['username']
        password = data['password']
        if User.objects.filter(username=username).exists():
            messages.success(request, _("Bunday foydalanuvchi avval ro'yxatdan o'tgan"))
            return HttpResponseRedirect(reverse_lazy('user:user-create'))

        region = Region.objects.get(id=int(data['region']))

        if data.get('is_superuser') == 'on':
            is_superuser = True
            is_staff = False
        else:
            is_superuser = False
            is_staff = True

        data['region'] = Region.objects.get(id=int(data['region']))

        user = User.objects.create(username=username, password=password, is_active=True, is_staff=is_staff,
                                   is_superuser=is_superuser)
        user.set_password(password)
        user.save()

        obj = self.model.objects.create(user=user, email=data['email'], phone=data['phone'], region=region)

        image = request.FILES.get('image')
        if image:
            obj.image = image

        # if is_superuser:
        #     assign_role(user, 'admin')
        # else:
        #     assign_role(user, 'staff')

        obj.save()
        return HttpResponseRedirect(self.success_url)


class UpdateCustomUserView(HasRoleMixin, UpdateView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    template_name = 'back/user/user_update.html'
    form_class = CreateCustomUserForm
    model = CustomUser
    context_object_name = 'object'
    success_url = reverse_lazy('user:user-list')

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        print(data, 'data')
        username = data['username']
        password = data['password']

        if data.get('is_superuser') == 'on':
            is_superuser = True
            is_staff = False
        else:
            is_superuser = False
            is_staff = True

        region = Region.objects.get(id=int(data['region']))

        data['region'] = Region.objects.get(id=int(data['region']))

        # obj = self.model.objects.create(user=user, email=data['email'], phone=data['phone'], region=region)
        obj = self.model.objects.get(id=self.kwargs['pk'])
        if User.objects.filter(username=username).exists():
            messages.success(request, _("Bunday foydalanuvchi avval ro'yxatdan o'tgan"))
            return HttpResponseRedirect(reverse_lazy('user:user-update', kwargs={'pk': obj.id}))

        obj.user.username = username
        obj.user.is_superuser = is_superuser
        obj.user.is_staff = is_staff
        obj.user.set_password(password)
        obj.user.save()

        obj.email = data['email']
        obj.phone = data['phone']
        obj.region = region

        image = request.FILES.get('image')
        if image:
            obj.image = image

        obj.save()
        return HttpResponseRedirect(self.success_url)


# class CustomUserList(views.SuperuserRequiredMixin, custom.CustomListView):
class CustomUserList(HasRoleMixin, custom.CustomListView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = CustomUser
    queryset = model.objects.filter(user__is_superuser=False)
    template_name = 'back/user/user_list.html'
    permission_required = 'auth.user.manage'


class CustomUserDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = 'admin'
    redirect_to_login = 'login'
    model = CustomUser
    success_url = reverse_lazy('user:user-list')
