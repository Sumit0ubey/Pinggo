from django.urls import path

from .views import ProfileView, ProfileEditView, ProfileSettingsView, ProfileDeleteView, ProfileEmailChangeView, ProfileEmailVerifyView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('@<username>/', ProfileView.as_view(), name='profile'),
    path('edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('onboarding/', ProfileEditView.as_view(), name='profile_onboarding'),
    path('settings/', ProfileSettingsView.as_view(), name='profile_settings'),
    path('emailchange/', ProfileEmailChangeView.as_view(), name='profile_email_change'),
    path('verify/', ProfileEmailVerifyView.as_view(), name='profile_verify'),
    path('delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]