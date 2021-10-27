from .models import User
from django.shortcuts import render, HttpResponse
# from django.contrib import messages
from django.contrib.auth import (
                                  authenticate,
                                  logout ,
                                  login
                              )
from django.shortcuts import (
                                  render,
                                  get_object_or_404,
                                  redirect
                              )
from .forms import (
                    RegistrationForm,
                    AccountAuthenticationForm,
                    AccountUpdateform
                )
from users.models import User


def registration_view(request):
    """
      Renders Registration Form 
    """
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        email    = request.POST.get('email')
        fname    = request.POST.get('fname')
        username  = request.POST.get('username')
        raw_pass = request.POST.get('password1')

        my_user = User.objects.create_user(username=username, email=email, fname=fname, password=raw_pass)
        my_user.save()
        # messages.success(request, "You have been Registered as {}".format(request.user.username))
    else:
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'users/signup.html', context)

    return render(request, "users/signup.html", context)

def logout_view(request):
    logout(request)
    # messages.success(request, "Logged Out")
    return redirect("/users/login")

def  login_view(request):

    context = {}
    user = request.user

    if user.is_authenticated:
        return HttpResponse("404 not found !")

    if request.POST:
        form    = AccountAuthenticationForm(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        user =  authenticate(email=email, password=password)

        if user:
            login(request, user)
            # messages.success(request, "Logged In")
            return redirect("/home")
        else:
            # messages.error("please Correct Below Errors")
            pass
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "users/login.html", context)


def account_view (request):

    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateform(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            # messages.success(request, "profile Updated")
        else:
            # messages.error(request, "Please Correct Below Errors")
            pass
    else:
        form  = AccountUpdateform(
            initial={
            'email':request.user.email,
            'username':request.user.username,
            }
        )
    context['account_form']=form

    return render(request, "main/profile.html", context)