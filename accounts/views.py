from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import views as auth_views


class CustomLoginView(auth_views.LoginView):
    """Custom LoginView with honeypot detection and simple session lockout."""
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):
        # Honeypot: silently reject submissions where 'website' is filled
        if request.POST.get('website'):
            form = self.get_form()
            form.add_error(None, "Bot detected.")
            return self.form_invalid(form)

        # Check session lockout
        lockout_ts = request.session.get('lockout_until')
        if lockout_ts and timezone.now().timestamp() < lockout_ts:
            form = self.get_form()
            form.add_error(None, "Too many failed attempts. Try again later.")
            return self.form_invalid(form)

        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        # Increment failed attempt counter
        count = self.request.session.get('failed_login_count', 0) + 1
        self.request.session['failed_login_count'] = count

        if count >= 5:
            # Lockout for 5 minutes
            until = timezone.now() + timedelta(minutes=5)
            self.request.session['lockout_until'] = until.timestamp()
            messages.error(self.request, "Too many failed attempts. Locked for 5 minutes.")
        else:
            messages.error(self.request, "Invalid login credentials.")

        return super().form_invalid(form)

    def form_valid(self, form):
        # Reset counters on success
        self.request.session.pop('failed_login_count', None)
        self.request.session.pop('lockout_until', None)
        return super().form_valid(form)


@login_required(login_url='login')
def profile_view(request):
    """Display user profile page."""
    user = request.user
    context = {
        'user': user,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined,
    }
    return render(request, 'accounts/profile.html', context)


def logout_view(request):
    """Handle user logout with confirmation."""
    if request.method == 'POST':
        logout(request)
        return redirect('logout_success')
    
    # GET request - show confirmation page
    return render(request, 'accounts/logout.html')


def logout_success(request):
    """Show logout success page."""
    return render(request, 'logout_success.html')
