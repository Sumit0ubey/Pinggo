from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, FormView, DeleteView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .exception import ProfileDoesNotExist
from .forms import ProfileForm, EmailForm
from .services.user_service import UserService
from .services.email_service import EmailService



class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')

        if username:
            context['profile'] = UserService.get_user_details_by_username(username)
        else:
            try:
                context['profile'] = UserService.get_user_details(self.request.user)
            except ProfileDoesNotExist:
                return redirect('account_login')

        return context


class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = "users/edit_profile.html"
    form_class = ProfileForm
    login_url = 'account_login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['onboarding'] = self.request.path == reverse_lazy('profile_onboarding')
        return context


class ProfileSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile_settings.html"
    login_url = 'account_login'


class ProfileEmailChangeView(LoginRequiredMixin, FormView):
    template_name = "partials/email_form.html"
    form_class = EmailForm
    login_url = 'account_login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        if EmailService.does_user_already_exist_by_email(user.id, new_email):
            messages.error(self.request, f'{new_email} already in use.')
            return redirect('profile_settings')

        if not EmailService.change_email(user, new_email):
            messages.error(self.request, 'Unable to change email. Please try again.')
            return redirect('profile_settings')

        messages.success(self.request, 'Email updated. Please verify it.')
        return redirect('profile_settings')

    def form_invalid(self, form):
        messages.warning(self.request, 'Invalid email.')
        return redirect('profile_settings')


class ProfileEmailVerifyView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        user = request.user
        email_service = EmailService()

        if not email_service.is_email_unverified(user):
            messages.info(request, 'Your email is already verified.')
            return redirect('profile_settings')

        if not email_service.send_verification_email(request):
            messages.error(request, 'Unable to send verification email. Please try again.')
            return redirect('profile_settings')

        messages.success(
            request,
            f'Verification email sent to {email_service.get_email_address()}.'
        )
        return redirect('profile_settings')


class ProfileDeleteView(LoginRequiredMixin, View):
    login_url = 'account_login'

    def get(self, request, *args, **kwargs):
        return render(request, "users/profile_delete.html")

    def post(self, request, *args, **kwargs):
        UserService.delete_user(request)
        messages.success(request, 'Account deleted.')
        return redirect('home')

