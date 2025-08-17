from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('verify', views.register_verify, name='register_verify'),
    path('resend-code/', views.resend_code, name='resend_code'),
    path('complate', views.register_complete, name='register_complete'),
    path('log_out', views.log_out, name='log_out'),
    path('login', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify_code/', views.verify_code, name='verify_code'),
    path('resent-reset-code/', views.resend_reset_code, name='resend_reset_code'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_change/', views.password_changed, name='password_changed'),
]