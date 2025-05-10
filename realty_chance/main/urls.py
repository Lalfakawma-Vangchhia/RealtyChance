from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/states/', views.state_list),
    path('upload/', views.upload_property, name='upload'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),

    path('login/', LoginView.as_view(template_name='main/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

] 