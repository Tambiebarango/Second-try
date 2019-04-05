from django.shortcuts import render
from . import forms

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'app5/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def signup(request):

    registered = False


    if request.method == "POST":
        user_form = forms.Userform(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user #oneonone relationship between user and profile

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            if 'portfolio_site' in request.FILES:
                profile.portfolio_site = request.FILES['portfolio_site']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
            user_form = forms.Userform()
            profile_form = forms.UserProfileInfoForm()
    return render(request, 'app5/signup.html',
                            {'Userform': user_form,
                            'UserProfileInfoForm': profile_form,
                            'registered': registered})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('special'))
            else:
                return HttpResponse("Account is not active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request,'app5/login.html',{})


@login_required
def special(request):
    return render(request, 'app5/special.html',{})











#
def help(request):
    return render(request, 'app5/helppage.html')
