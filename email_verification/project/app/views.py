from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
import secrets
from datetime import timedelta
import logging
from .forms import SignUpForm
from .models import Profile

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def signup(request):
    # Rate limiting check
    ip_address = request.META.get('REMOTE_ADDR')
    if cache.get(f'signup_attempts_{ip_address}', 0) >= 3:
        messages.error(request, 'Too many signup attempts. Please try again later.')
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User must verify email before activation
            user.save()

            # Generate verification token
            token = secrets.token_urlsafe(32)
            expiry = timezone.now() + timedelta(days=1)
            
            # Save token to profile
            profile = user.profile
            profile.verification_token = token
            profile.token_expiry = expiry
            profile.save()

            # Send verification email
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': token})
            )
            
            send_mail(
                'Verify your email',
                f'Please click the following link to verify your email: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            try:
                # Generate verification token
                token = secrets.token_urlsafe(32)
                expiry = timezone.now() + timedelta(days=1)
                
                # Save token to profile
                profile = user.profile
                profile.verification_token = token
                profile.token_expiry = expiry
                profile.save()

                # Send verification email
                verification_link = request.build_absolute_uri(
                    reverse('verify_email', kwargs={'token': token})
                )
                
                send_mail(
                    'Verify your email',
                    f'Please click the following link to verify your email: {verification_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                # Increment rate limit counter
                cache.set(f'signup_attempts_{ip_address}', 
                         cache.get(f'signup_attempts_{ip_address}', 0) + 1, 
                         timeout=3600)  # 1 hour timeout

                messages.success(request, 'Account created! Please check your email to verify your account.')
                logger.info(f'New user signup: {user.email}')
                return redirect('home')

            except Exception as e:
                logger.error(f'Error during signup: {str(e)}')
                messages.error(request, 'An error occurred during signup. Please try again.')
                return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@require_http_methods(["GET"])
def verify_email(request, token):
    try:
        profile = Profile.objects.filter(verification_token=token).first()
        
        if not profile:
            messages.error(request, 'Invalid verification link')
            logger.warning(f'Invalid verification token attempt: {token}')
            return redirect('home')
            
        if timezone.now() > profile.token_expiry:
            messages.error(request, 'Verification link has expired')
            logger.warning(f'Expired verification token attempt: {token}')
            return redirect('home')
            
        profile.user.is_active = True
        profile.email_verified = True
        profile.verification_token = ''
        profile.save()
        
        login(request, profile.user)
        messages.success(request, 'Email verified successfully!')
        logger.info(f'Email verified for user: {profile.user.email}')
        return redirect('home')
        
    except Exception as e:
        logger.error(f'Error during email verification: {str(e)}')
        messages.error(request, 'An error occurred during verification. Please try again.')
        return redirect('home')

def home(request):
    return render(request, 'home.html')
