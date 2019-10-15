from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
)
from thebrushstash.models import OtherImage


class AboutTheStoryView(TemplateView):
    template_name = 'thebrushstash/about_the_story.html'


class FaqView(TemplateView):
    template_name = 'thebrushstash/faq.html'


class GeneralTermsAndConditions(TemplateView):
    template_name = 'thebrushstash/general_terms_and_conditions.html'


class TakingCareOfYourBrushView(TemplateView):
    template_name = 'thebrushstash/brush_care.html'


class OtherImageView(LoginRequiredMixin, TemplateView):
    template_name = 'thebrushstash/other_images.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'other_images': OtherImage.objects.all()})
        return context
