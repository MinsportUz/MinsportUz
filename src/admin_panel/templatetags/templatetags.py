import datetime
import re

from django import template
from django.core.serializers import serialize
from django.utils.timezone import now
from modeltranslation.utils import get_language

from admin_panel.model.territorial import Region
import json
from django.core.serializers.json import DjangoJSONEncoder
#model
from admin_panel.model import contact, settings


register = template.Library()


@register.simple_tag(name='get_language_url')
def get_language_url(request, lang):
    active_language = get_language()
    return request.get_full_path().replace(active_language, lang, 1)

@register.simple_tag(name='get_count_contacts_notifications')
def get_count_contacts_notifications():
    contacts = contact.Contact.objects.all().filter(status=0)

    return int(contacts.count())
   
@register.simple_tag(name='get_count_feedback_notifications')
def get_count_feedback_notifications():
    feedbacks = contact.Feedback.objects.all().filter(status=0)
    return int(feedbacks.count())



@register.simple_tag(name='get_regions')
def get_regions():
    return Region.objects.all()


@register.filter
def json(queryset):
    return serialize('json', queryset)