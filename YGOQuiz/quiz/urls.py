from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('random-image-info/', views.random_image_info, name='random_image_info'),
    path('fetch-image/', views.fetch_image, name='fetch_image')
]
