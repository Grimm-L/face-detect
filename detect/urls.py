from django.urls import path

from . import views

urlpatterns = [
    path('', views.detect, name='detect'),
    path('menu', views.menu_api_demo, name='menu_api_demo'),
    path('dev_api', views.detect_dev_api, name='web page detect dev api')
]