from django.http import HttpResponseRedirect
from django.utils import translation

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

    # class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    #
    #     """
    #     Ignore Accept-Language HTTP headers
    #
    #     This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    #     as the default initial language, unless another one is set via sessions or cookies
    #
    #     Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    #     namely django.middleware.locale.LocaleMiddleware
    #     """
    # def process_request(self, request):
    #     if 'HTTP_ACCEPT_LANGUAGE' in request.META:
    #         del request.META['HTTP_ACCEPT_LANGUAGE']


def force_default_language_middleware(get_response):
    """
        Ignore Accept-Language HTTP headers

        This will force the I18N machinery to always choose settings.LANGUAGE_CODE
        as the default initial language, unless another one is set via sessions or cookies

        Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
        namely django.middleware.locale.LocaleMiddleware
        """

    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware


class CustomLocaleMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Redirect /en/*** url into uz. Therefore site will be availabe without en anytime using __call__ function
        """
        lang = str(request.path)
        lang = lang.split('/')
        if lang[1] == 'en':
            path = request.path
            path = path.replace("/en/", "/uz/", 1)
            return HttpResponseRedirect(path)

        """
        Middleware look at the language header.
        If header has 'oz' then replace it to 'sr' which is available in Django and outcome will be in 'sr'
        """

        language_code = 'sr'
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            if request.META['HTTP_ACCEPT_LANGUAGE'] == 'oz':
                translation.activate(language_code)

        response = self.get_response(request)

        # translation.deactivate()

        return response
