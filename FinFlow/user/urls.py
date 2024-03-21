from django.urls import path, include
from .views import Logout_View
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', Logout_View, name='logout'),
        
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('api/v1/id-validation', views.IdValidation.as_view(), name='id_validation'), 
    path('api/v1/hp-validation', views.HPValidation.as_view(), name='hp_validation'), 
    path('api/v1/auth-message', views.AuthView.as_view(), name='auth_message'), 
]