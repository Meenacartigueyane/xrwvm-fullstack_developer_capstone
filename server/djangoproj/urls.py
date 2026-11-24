
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django API routes
    path('djangoapp/', include('djangoapp.urls')),

    # React application pages
    path('', TemplateView.as_view(template_name='index.html')),
    path('dealers/', TemplateView.as_view(template_name='index.html')),
    path('dealer/&lt;int:dealer_id&gt;', TemplateView.as_view(template_name='index.html')),
    path('postreview/&lt;int:dealer_id&gt;', TemplateView.as_view(template_name='index.html')),
    path('login', TemplateView.as_view(template_name='index.html')),
    path('register', TemplateView.as_view(template_name='index.html')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
