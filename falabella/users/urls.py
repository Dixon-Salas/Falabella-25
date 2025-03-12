from django.urls import path
from .views import UserListCreateView, UserDetailView, ChangePasswordView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('users/',UserListCreateView.as_view(),name='user-list'),
    path('users/<int:pk>/',UserDetailView.as_view(),name='user-detail'),
    path('users/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('users/reset_password/', ResetPasswordView.as_view(), name='reset_password'),
]
