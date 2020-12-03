from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path, reverse_lazy

from shop.api.urls import shop_api_urls
from thebrushstash.api.urls import thebrushstash_api_urls
from thebrushstash.constants import (
    ABOUT,
    BRUSH_CARE,
    CONTACT,
    PAYMENT_DELIVERY,
    COMPLAINTS,
    TOS,
)
from account.views import LoginOverrideView
from shop.views import (
    CheckoutView,
    IPGPurchaseCancelledView,
    IPGPurchaseCompletedView,
    PurchaseCompletedView,
    ReviewBagView,
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
    RegionView,
)

# may not be suffixed by language code
urlpatterns = [
    path('reset/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(
        post_reset_login=True,
        success_url=reverse_lazy('shop:shop')
    ), name='password_reset_confirm'),
    path('login/', LoginOverrideView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('api/', include((shop_api_urls + thebrushstash_api_urls, 'api'), namespace='api')),
    path('test-images/', TestImageView.as_view(), name='other-images'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('region/', RegionView.as_view(), name='region'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('review-bag/', ReviewBagView.as_view(), name='review-bag'),

    path('purchase-completed/', PurchaseCompletedView.as_view(), name='purchase-completed'),
    path('ipg-purchase-completed/', IPGPurchaseCompletedView.as_view(), name='ipg-purchase-completed'),
    path('ipg-purchase-cancelled/', IPGPurchaseCancelledView.as_view(), name='ipg-purchase-cancelled'),
]
urlpatterns += i18n_patterns(
    path('faq/', FaqView.as_view(), name='faq'),

    path('{}/'.format(ABOUT), AboutTheStoryView.as_view(), name=ABOUT),
    path('{}/'.format(BRUSH_CARE), TakingCareOfYourBrushView.as_view(), name=BRUSH_CARE),
    path('{}/'.format(CONTACT), ContactView.as_view(), name=CONTACT),
    path('{}/'.format(PAYMENT_DELIVERY), PaymentAndDeliveryView.as_view(), name=PAYMENT_DELIVERY),
    path('{}/'.format(COMPLAINTS), ReturnsAndComplaintsView.as_view(), name=COMPLAINTS),
    path('{}/'.format(TOS), GeneralTermsAndConditions.as_view(), name=TOS),

    path('', include(('shop.urls', 'shop'), namespace='shop')),
    prefix_default_language=False,
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_url = '/preview/'
admin.site.site_header = 'The Brush Stash Webshop'
admin.site.site_title = 'The Brush Stash Webshop'
admin.site.enable_nav_sidebar = False

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
