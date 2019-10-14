"""
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from thebrushstash.views import (
    AboutTheStoryView,
    FaqView,
    OtherImageView,
    TakingCareOfYourBrushView,
)
from thebrushstash.constants import (
    about_the_story_slug,
    brush_care_slug,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path(
        '{}/'.format(about_the_story_slug),
        AboutTheStoryView.as_view(),
        name=about_the_story_slug
    ),
    path('faq/', FaqView.as_view(), name='faq'),
    path(
        '{}/'.format(brush_care_slug),
        TakingCareOfYourBrushView.as_view(),
        name=brush_care_slug
    ),
    path('other-images/', OtherImageView.as_view(), name='other-images'),
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
