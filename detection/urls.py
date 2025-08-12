from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from .views import predict_image

urlpatterns = [
    path('predict/', predict_image, name='predict'),
    path('', views.predict_image, name='predict_image'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='detection/login.html',next_page='/detection/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
