# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from uglymirror.forms import SignUpForm
from uglymirror.models import UglyMirror
from uglymirror.tokens import account_activation_token

# Create your views here.

# class home(LoginRequiredMixin, generic.ListView):

#   login_url = '/login/'
#   redirect_field_name = 'redirect_to'
#   template_name = 'home.html'
#   context_object_name = 'all_jobs'

#   def get_queryset(self):
#     return True

class UglyForm(ModelForm):
  class Meta:
    model = UglyMirror
    fields = ['age', 'ugly_rate', 'feeling', 'interface_compare']


# def home(request, template_name='home.html'):
#   if request.method == 'GET':
#     return render(request, 'home.html')

@login_required()
def ugly_list(request, template_name='ugly_mirror/ugly_list.html'):
  if request.user.is_superuser:
    uglymirror = UglyMirror.objects.all()
  else:
    uglymirror = UglyMirror.objects.filter(user=request.user)
  data = {}
  data['object_list'] = uglymirror
  return render(request, template_name, data)

@login_required()
def ugly_create(request, template_name='ugly_mirror/ugly_form.html'):
  form = UglyForm(request.POST or None)
  if form.is_valid():
    uglymirror = form.save(commit=False)
    uglymirror.user = request.user
    uglymirror.save()
    return redirect('ugly_list')
  return render(request, template_name, {'form':form})


@login_required()
def ugly_update(request, pk, template_name='ugly_mirror/ugly_form.html'):
  if request.user.is_superuser:
    uglymirror = get_object_or_404(UglyMirror, pk=pk)
  else:
    uglymirror = get_object_or_404(UglyMirror, pk=pk, user=request.user)
  form = UglyForm(request.POST or None, instance=uglymirror)
  if form.is_valid():
    form.save()
    return redirect('ugly_list')
  return render(request, template_name, {'form':form})

@login_required()
def ugly_delete(request, pk, template_name='ugly_mirror/ugly_confirm_delete.html'):
  if request.user.is_superuser:
    uglymirror = get_object_or_404(UglyMirror, pk=pk)
  else:
    uglymirror = get_object_or_404(UglyMirror, pk=pk, user=request.user)
  if request.method == 'POST':
    uglymirror.delete()
    return redirect('ugly_list')
  return render(request, template_name, {'object':uglymirror})


def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.is_active = False
      user.save()
      current_site = get_current_site(request)
      subject = 'Activate Your Uglymirror Account'
      protocol = 'https'
      if request.is_secure:
        protocol = 'http'
      message = render_to_string('account_activation_email.html', {
              'user': user,
              'domain': current_site.domain,
              'protocol': protocol,
              'uid': urlsafe_base64_encode(force_bytes(user.pk)),
              'token': account_activation_token.make_token(user),
          })
      user.email_user(subject, message)
      return redirect('account_activation_sent')
  else:
    form = SignUpForm()
  return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.profile.email_confirmed = True
    user.save()
    return redirect('user_ready_to_login')
  else:
    return render(request, 'account_activation_invalid.html')

def user_ready_to_login(request):
  return render(request, 'user_ready_to_login.html')

# def signup(request):
#   if request.method == 'POST':
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#       form.save()
#       username = form.cleaned_data.get('username')
#       raw_password = form.cleaned_data.get('password1')
#       user = authenticate(username=username, password=raw_password)
#       login(request, user)
#       return redirect('ugly_list')
#   else:
#     form = SignUpForm()
#   return render(request, 'signup.html', {'form': form})
