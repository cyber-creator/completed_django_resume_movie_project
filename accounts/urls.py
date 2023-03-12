from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signin/', views.account_sign_in, name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='signout'),
    path('signup/', views.account_register, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

