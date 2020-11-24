from django.conf import settings
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
)
from django.views.generic.list import ListView
from django.views.generic import TemplateView, View
from django.utils import translation

from thebrushstash.constants import (
    ABOUT,
    COMPLAINTS,
    CONTACT,
    DEFAULT_REGION,
    PAYMENT_DELIVERY,
    TOS,
    BRUSH_CARE,
)
from thebrushstash.models import (
    QandAPair,
    Region,
    StaticPageContent,
    TestImage,
)


class AboutTheStoryView(TemplateView):
    template_name = 'thebrushstash/about_the_story.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_content = StaticPageContent.objects.get(slug=ABOUT)
        context.update({
            'title': sp_content.title,
            'title_cro': sp_content.title_cro,
            'content': sp_content.content,
            'content_cro': sp_content.content_cro,
        })
        return context


class ContactView(TemplateView):
    template_name = 'thebrushstash/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_content = StaticPageContent.objects.get(slug=CONTACT)
        context.update({
            'title': sp_content.title,
            'title_cro': sp_content.title_cro,
            'content': sp_content.content,
            'content_cro': sp_content.content_cro,
        })
        return context


class FaqView(TemplateView):
    template_name = 'thebrushstash/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'faq_pairs': QandAPair.objects.all(),
        })
        return context


class GeneralTermsAndConditions(TemplateView):
    template_name = 'thebrushstash/general_terms_and_conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_content = StaticPageContent.objects.get(slug=TOS)
        context.update({
            'title': sp_content.title,
            'title_cro': sp_content.title_cro,
            'content': sp_content.content,
            'content_cro': sp_content.content_cro,
        })
        return context


class ReturnsAndComplaintsView(TemplateView):
    template_name = 'thebrushstash/returns_and_complaints.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_content = StaticPageContent.objects.get(slug=COMPLAINTS)
        context.update({
            'title': sp_content.title,
            'title_cro': sp_content.title_cro,
            'content': sp_content.content,
            'content_cro': sp_content.content_cro,
        })
        return context


class PaymentAndDeliveryView(TemplateView):
    template_name = 'thebrushstash/payment_and_delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_content = StaticPageContent.objects.get(slug=PAYMENT_DELIVERY)
        context.update({
            'title': sp_content.title,
            'title_cro': sp_content.title_cro,
            'content': sp_content.content,
            'content_cro': sp_content.content_cro,
        })
        return context


class TakingCareOfYourBrushView(TemplateView):
    template_name = 'thebrushstash/brush_care.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sp_content = StaticPageContent.objects.get(slug=BRUSH_CARE)
        context.update({
            'title': sp_content.title,
            'title_cro': sp_content.title_cro,
            'content': sp_content.content,
            'content_cro': sp_content.content_cro,
        })
        return context


class TestImageView(ListView):
    model = TestImage
    template_name = 'shop/test_images.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class RegionView(View):
    def post(self, request, *args, **kwargs):
        region = Region.objects.get(name=request.POST.get('region', DEFAULT_REGION))
        request.session['region'] = region.name
        request.session['currency'] = region.currency
        translation.activate(region.language)

        next_url = request.GET.get('next', '/')
        if region.language != 'hr':
            next_url = next_url.replace('/hr', '')
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANG_COOKIE_NAME_INTERNAL, region.language)

        return response
