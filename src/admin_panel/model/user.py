# from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rolepermissions.roles import assign_role

from . import territorial


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(territorial.Region, on_delete=models.CASCADE, null=True)
    email = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    image = models.FileField(upload_to='user', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_custom(sender, instance, created, **kwargs):
        if created:
            # if instance.is_superuser:
            #     group = Group.objects.filter(name='admin')
            #     if not group.exists():
            #         group = Group.objects.create(name='admin')
            # else:
            #     group = Group.objects.filter(name='staff')
            #     if not group.exists():
            #         group = Group.objects.create(name='staff')
            #
            if instance.is_superuser:
                assign_role(instance, 'admin')
            else:
                assign_role(instance, 'staff')



    # def save(self, *args, **kwargs):
    #
    #     created = self.id is None
    #     super(CustomUser, self).save(*args, **kwargs)
    #
    #     # after save user has ID
    #     # add user to group only after creating
    #     if created:
    #         if self.user.is_superuser:
    #             g = Group.objects.get(name='Some Group')
    #             g.user_set.add(sender)



    def __str__(self):
        return str(self.user)
