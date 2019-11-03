from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from thebrushstash.api.urls import api_urls
from thebrushstash.constants import (
    ABOUT,
    BRUSH_CARE,
    CONTACT,
    PAYMENT_DELIVERY,
    RETURNS_COMPLAINTS,
    TOS,
)
from thebrushstash.views import (
    AboutTheStoryView,
    ContactView,
    FaqView,
    GeneralTermsAndConditions,
    PaymentAndDeliveryView,
    ReturnsAndComplaintsView,
    TakingCareOfYourBrushView,
    TestImageView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('api/', include((api_urls, 'api'), namespace='api')),
    path('i18n/', include('django.conf.urls.i18n')),

    path('faq/', FaqView.as_view(), name='faq'),
    path('{}/'.format(ABOUT), AboutTheStoryView.as_view(), name=ABOUT),
    path('{}/'.format(BRUSH_CARE), TakingCareOfYourBrushView.as_view(), name=BRUSH_CARE),
    path('{}/'.format(CONTACT), ContactView.as_view(), name=CONTACT),
    path('{}/'.format(PAYMENT_DELIVERY), PaymentAndDeliveryView.as_view(), name=PAYMENT_DELIVERY),
    path('{}/'.format(RETURNS_COMPLAINTS), ReturnsAndComplaintsView.as_view(), name=RETURNS_COMPLAINTS),
    path('{}/'.format(TOS), GeneralTermsAndConditions.as_view(), name=TOS),

    path('', include('django.contrib.auth.urls')),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('test-images/', TestImageView.as_view(), name='other-images'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'The Brush Stash'
admin.site.site_title = 'The Brush Stash'

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
