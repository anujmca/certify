from django.urls import path, re_path
from django.contrib import admin


from . import views


admin.autodiscover()

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('certificates/generate', views.generate_certificate, name='generate_certificate'),
]

