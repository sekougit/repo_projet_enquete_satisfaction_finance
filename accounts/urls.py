from django.urls import path
from . import views
from .views import change_password_view, profile_view, forgot_password_view
from .views import CustomLoginView

urlpatterns = [

    path('profile/', profile_view, name='profile'),
        path(
        'change-password/',
        change_password_view,
        name='change_password'
    ),
        path(
        'forgot-password/',
        forgot_password_view,
        name='forgot_password'
    ),
        path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),
    path('logout/', views.logout_view, name='logout'),
]