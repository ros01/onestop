from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView
from django.contrib.auth import get_user_model, update_session_auth_hash, authenticate, login as auth_login
from django.contrib import messages, auth
from .forms import SignupForm

AUTH_USER_MODEL = 'accounts.User'

#User = get_user_model()

class LoginTemplateView(TemplateView):
    template_name = "accounts/login.html"


class SignUpView(View):
    form_class = SignupForm
    template_name = 'accounts/register.html'
    template_name1 = 'accounts/account_creation_confirmation.html'
    
    

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

   

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            #user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            

            return render(request, self.template_name1)

        return render(request, self.template_name, {'form': form})


def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)
    if user is not None:
        auth_login(request, user)
        
        if user.department == 'Monitoring':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Registrars Office':
            return redirect('rrbnstaff:staff_dashboard')

        #if user.department == 'Monitoring':
            #return redirect('store:store_dashboard')
        if user.department == 'Registrations':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Hr':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Procurement':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Finance':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Audit':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'ICT':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Stores':
            return redirect('rrbnstaff:staff_dashboard')
        if user.department == 'Protocol':
            return redirect('rrbnstaff:staff_dashboard')
        if user.role == 'Fleet Managment':
            return redirect('fleet:fleet_dashboard')
        if user.role == 'Human Resources':
            return redirect('hr:hr_dashboard')
        if user.role == 'Procurement':
            return redirect('store:store_dashboard')
        if user.role == 'Registrars':
            return redirect('store:store_dashboard')
        if user.role == 'Stores':
            return redirect('store:store_dashboard')
        if user.role == 'RRBN Staff':
            return redirect('rrbnstaff:staff_dashboard')
    else:
        messages.error(request, 'Please enter the correct email and password for your account. Note that both fields may be case-sensitive.')
        return redirect('accounts:signin')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')
