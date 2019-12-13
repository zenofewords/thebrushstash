from django.utils.translation import get_language


def set_currency_middleware(get_response):
    def middleware(request):
        language = get_language()

        if not request.session.get('currency'):
            request.session['currency'] = 'eur' if language != 'hr' else 'hrk'

        response = get_response(request)
        return response

    return middleware
