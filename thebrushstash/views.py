from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic import TemplateView

from thebrushstash.models import TestImage


class AboutTheStoryView(TemplateView):
    template_name = 'thebrushstash/about_the_story.html'


class ContactView(TemplateView):
    template_name = 'thebrushstash/contact.html'


class FaqView(TemplateView):
    template_name = 'thebrushstash/faq.html'


class GeneralTermsAndConditions(TemplateView):
    template_name = 'thebrushstash/general_terms_and_conditions.html'


class ReturnsAndComplaintsView(TemplateView):
    template_name = 'thebrushstash/returns_and_complaints.html'


class PaymentAndDeliveryView(TemplateView):
    template_name = 'thebrushstash/payment_and_delivery.html'


class TakingCareOfYourBrushView(TemplateView):
    template_name = 'thebrushstash/brush_care.html'


class TestImageView(LoginRequiredMixin, ListView):
    model = TestImage
    template_name = 'shop/test_images.html'
