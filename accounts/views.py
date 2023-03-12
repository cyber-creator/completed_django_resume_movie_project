from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import FormLogin, FormRegistration, FormUpdateUser, FormUpdateProfile, FormChangePassword, FormUpdateAvatar
from django.contrib import messages
from .models import Profile
from films.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def account_sign_in(request):
    if request.method == 'POST':
        form = FormLogin(request.POST)

        if form.is_valid():
            account_record = None
            cd = form.cleaned_data

            try:
                account_record = User.objects.get(email=cd['email'])
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return redirect('signin')

            if account_record:
                user = authenticate(request, username=account_record, password=cd['password'])

                if user is not None:
                    login(request, user)
                    return redirect('films:home')

            messages.error(request, 'Incorrect email or password')

    else:
        form = FormLogin()
    return render(request, 'profile/signin.html', {'form': form})


def account_register(request):
    if request.method == 'POST':
        form = FormRegistration(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            email = cd['email']
            password = cd['password']
            password2 = cd['password2']

            if User.objects.filter(username=cd['first_name']).exists():
                messages.error(request, 'Username name already in use')
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use')
                return redirect('signin')

            if password == password2:
                new_account = User.objects.create_user(username=first_name, email=email, password=password)
                Profile.objects.create(user=new_account)
                # new_account.save()
                login(request, new_account)
                return redirect('films:home')
            else:
                messages.error(request, 'Password does\'t match')
                return redirect('signup')

    else:
        form = FormRegistration()
    return render(request, 'profile/signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST' and 'save' in request.POST:
        user = None
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('profile')

        if user is None or user.id == request.user.id:
            user_data = FormUpdateUser(instance=request.user, data=request.POST)
            profile_data = FormUpdateProfile(instance=request.user.profile, data=request.POST)

            if user_data.is_valid() and profile_data.is_valid():
                user_data.save()
                profile_data.save()

                messages.success(request, 'Profile was update')
        else:
            messages.error(request, 'User with this email exist')
        return redirect('profile')

    elif request.method == 'POST' and 'change' in request.POST:
        user = None
        form = FormChangePassword(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            try:
                user = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                pass

            if user is None or request.user.id:
                old_password = cd['passwordOld']
                new_password = cd['passwordNew']
                confirm_password = cd['passwordConf']

                if user.check_password(old_password) and new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    login(request, user)

                    messages.success(request, 'Password was update')
                else:
                    messages.error(request, 'Sorry something don\'t match')
                return redirect('profile')

    elif request.method == 'POST' and 'profile_img' in request.FILES:
        user_profile = Profile.objects.get(user=request.user)

        form_avatar = FormUpdateAvatar(data=request.POST, instance=user_profile)

        if form_avatar.is_valid():
            form_val = form_avatar.save(commit=False)
            form_val.user = request.user

            if 'profile_img' in request.FILES:
                form_val.profile_img = request.FILES['profile_img']

            form_val.save()

        return redirect('profile')

    else:
        user_data = FormUpdateUser(instance=request.user)
        profile_data = FormUpdateProfile(instance=request.user.profile)
        password_update = FormChangePassword()

    profile_movie = Film.objects.filter(selected=request.user).order_by('-id')
    paginator = Paginator(profile_movie, 12)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if page_obj:
        return render(request, 'profile/profile.html', {'user_data': user_data, 'profile_data': profile_data,
                                                        'password_update': password_update,
                                                        'page_obj': page_obj, 'profile_movie': profile_movie})
    else:
        return render(request, 'profile/profile.html', {'user_data': user_data, 'profile_data': profile_data,
                                                        'password_update': password_update,
                                                        'message': "Sorry no results were found"})


