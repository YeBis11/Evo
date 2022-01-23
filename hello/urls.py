from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('profile/<str:pk>', user_profile, name='profile'),
    path('', index, name='home'),
    path('email/', email, name='email'),
    path('update/<str:pk>', update_email, name='update'),
    path('delete/<str:pk>', delete_email, name='delete'),
    path('delete-message/<str:pk>', delete_message, name='delete-message'),
    path('email/show/<str:pk>', show_email_info, name='show'),
    path('greet/', greet, name='greet')
]
