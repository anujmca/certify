from django.urls import path, re_path
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from . import views_restful


admin.autodiscover()

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('certificates/generate', views_restful.generate_certificate, name='generate_certificate'),
    path('certificates/publish', views_restful.publish_certificates, name='publish_certificates'),
    path('certificates/<int:pk>/publish', views_restful.publish_certificate, name='publish_certificate'),


    path('events/', views_restful.EventList.as_view()),
    path('events/<int:pk>/', views_restful.EventDetail.as_view()),

    path('templates/', views_restful.TemplateList.as_view()),
    path('templates/<int:pk>/', views_restful.TemplateDetail.as_view()),

    path('datasheets/', views_restful.DataSheetList.as_view()),
    path('datasheets/<int:pk>/', views_restful.DataSheetDetail.as_view()),
]

