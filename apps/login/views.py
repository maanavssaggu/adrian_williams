from django.shortcuts import render, redirect
from scraper.Auth import Auth
from django import forms
from django.conf import settings

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Email', 'style': 'width: 600px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'style': 'width: 600px;'}))


def login(request):
    # Create Login form
    context = {}
    context['form']= LoginForm()

    # If we are getting here after entering incorrect credentials, display error message, remove flag for refreshes
    if (settings.ENTERED_INCORRECT_CREDENTIALS):
        context['error'] = "Invalid Email or Password"
        settings.ENTERED_INCORRECT_CREDENTIALS = False

    return render(request, "login/login.html", context)

def verify_user(request):
    # Make sure we are getting here from a POST request
    if request.method == "POST":
        # Ensure the form is valid
        request_form = LoginForm(request.POST)
        if request_form.is_valid():
            # If so, authenticate the user
            email = request_form.cleaned_data["email"]
            password = request_form.cleaned_data["password"]
            auth = Auth()

            # When valid, redirect to home page and reset flags
            if auth.authenticate_user_with_email_and_password(email, password):
                settings.LOGGED_IN = True
                settings.ENTERED_INCORRECT_CREDENTIALS = False
                return redirect("/home/")
            
        settings.ENTERED_INCORRECT_CREDENTIALS = True
        return redirect("/")
    
    # If get request, just redirect
    return redirect("/")

