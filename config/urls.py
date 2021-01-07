"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Get the global variables to dynamically set the admin url
import environ # New 20210103
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()


urlpatterns = [
    # Django admin
    path(env("DJANGO_ADMIN_URL"), admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # Local apps
    path('', include('pages.urls')),
#    path('books/', include('books.urls')),
    path('customers/', include('customer.urls')),
    path('clocktypes/', include('clocktype.urls')),
    path('clocks/', include('clock.urls')),
    path('repairer/', include('repairer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Use the debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
