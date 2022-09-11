from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),  
]
if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
