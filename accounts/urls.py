from django.urls import path
from .views import register, logout_view, logout_success, profile_view, CustomLoginView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('logout-success/', logout_success, name='logout_success'),
]
