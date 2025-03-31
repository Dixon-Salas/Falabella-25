from django.urls import path
from .views import UserListCreateView, UserDetailView, ChangePasswordView, ForgotPasswordView, ResetPasswordView, AddressListCreateView, AddressDetailView, UserProfileView

urlpatterns = [
    path('users/',UserListCreateView.as_view(),name='user-list'),
    path('users/<int:pk>/',UserDetailView.as_view(),name='user-detail'),
    path('users/change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('users/reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path("addresses/", AddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]
