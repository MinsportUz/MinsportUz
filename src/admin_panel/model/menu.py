from django.db import models

from admin_panel.common import generate_field


class Menu(models.Model):
    title = models.CharField(max_length=300)
    url = models.CharField(max_length=500, null=True)
    order = models.IntegerField(null=True, blank=True)
    sub_order = models.IntegerField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    is_static = models.BooleanField(default=False, blank=True)
    footer = models.BooleanField(default=False, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'menus'
        ordering = ['order']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    # def save(self, *args, **kwargs):
    #     if self.url and self.is_static:
    #         self.url = 'static/' + self.url
    #         super(Menu, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Menu, self).save(*args, **kwargs)
