from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/states/', views.state_list),
    path('upload/', views.upload_property, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),

] 