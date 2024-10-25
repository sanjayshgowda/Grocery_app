from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Include store app's URLs
    
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)