"""certify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from certify import views

urlpatterns = [
    path('services/', include('services.urls')),
    path('admin/', admin.site.urls),
    path('login', views.login, name='login'),
    path('', views.index, name='index'),

    path('templates', views.templates, name='templates'),
    path('certificates', views.certificates, name='certificates'),
    # path('certificates', views.CertificateTableView, name='certificates'),
    path('employees', views.employees, name='employees'),
]

from django.conf.urls.static import static
from certify import settings
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
