from django.urls import path, re_path
from django.contrib import admin
from . import views_restful


admin.autodiscover()

urlpatterns = [
    # path('login', views.login, name='login'),
    # path('logout', views.logout, name='logout'),

    path('certificates/', views_restful.PublicCertificateList.as_view()),
    path('certificates/<int:pk>/', views_restful.PublicCertificateDetail.as_view()),
]

