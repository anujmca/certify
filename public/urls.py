from django.urls import path, re_path
from django.contrib import admin
from . import views_restful, views


admin.autodiscover()

urlpatterns = [
    # path('login', views.login, name='login'),
    # path('logout', views.logout, name='logout'),

    path('certificates/', views_restful.PublicCertificateList.as_view()),
    path('certificates/<int:pk>/', views_restful.PublicCertificateDetail.as_view()),
    path('certificates/<int:pk>/view', views.public_certificate_view, name='public_certificate_view'),
    path('certificates/<int:pk>/view/raw', views.public_certificate_view_raw, name='public_certificate_view_raw'),
    path('certificates/<int:pk>/download', views.public_certificate_download, name='public_certificate_download'),
]

