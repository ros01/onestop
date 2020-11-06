from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', include ('pages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('rrbnstaff/', include('rrbnstaff.urls')),
    path('store/', include('store.urls')),
    path('fleet/', include('fleet.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
