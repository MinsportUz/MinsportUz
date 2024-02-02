from django.utils.text import slugify
from api import translate

# GENERATE UNIQUE SLUG
def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


# Simple boolean checke for HTML checker
def boolen_checker(value):
    if value == "on":
        return True
    return False


# Auto generate model
def generate_field(field):
    try:
        result = translate.translate_to_latin(field)
        return result
    except Exception:
        pass