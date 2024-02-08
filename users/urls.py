from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, FeedbackCreateView,
                         FeedbackDetailView, FeedbackListView, UserLoginView,
                         UserProfileView, UserRegistrationView)

app_name = 'users'

urlpatterns = [
    # path('login/', login, name='login'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('registration/', registration, name='registration'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    # path('profile/', profile, name='profile'),
    # path('profile/', login_required(UserProfileView.as_view()), name='profile'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # path('logout/', logout, name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='email_verification'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('add-feedback/', FeedbackCreateView.as_view(), name='add_feedback'),
    path('feedback/<int:pk>', FeedbackDetailView.as_view(), name='feedback_detail'),
]
