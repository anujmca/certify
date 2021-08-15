from django.urls import path, re_path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from . import views_restful


admin.autodiscover()

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('certificates/generate', views.generate_certificate, name='generate_certificate'),

    path('events/', views_restful.EventList.as_view()),
    path('events/<int:pk>/', views_restful.EventDetail.as_view()),
]

