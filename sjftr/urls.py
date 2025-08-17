
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def chrome_devtools_json(request):
    return JsonResponse({
        "status": "ok",
        "description": "Chrome DevTools config placeholder"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('account.urls')),
    path('', include('main.urls')),
    path('.well-known/appspecific/com.chrome.devtools.json', chrome_devtools_json),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
