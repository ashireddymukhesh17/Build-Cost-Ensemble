from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .models import User


def home(request):

    return render(
        request,
        'users/home.html'
    )


def register(request):

    if request.method == 'POST':

        user_name = request.POST['user_name']

        password = request.POST['password']

        mobile_number = request.POST['mobile_number']

        place = request.POST['place']


        # Check username already exists

        if User.objects.filter(
            user_name=user_name
        ).exists():

            return render(
                request,
                'users/register.html',
                {
                    'error': 'Username already exists'
                }
            )


        # Create user

        user = User(

            user_name=user_name,

            password=make_password(password),

            mobile_number=mobile_number,

            place=place

        )


        user.save()


        return redirect('login')


    return render(
        request,
        'users/register.html'
    )


def login_view(request):

    if request.method == 'POST':

        user_name = request.POST['user_name']

        password = request.POST['password']


        try:

            user = User.objects.get(
                user_name=user_name
            )


            if check_password(
                password,
                user.password
            ):

                request.session['user_id'] = user.id

                request.session['user_name'] = user.user_name

                return redirect('dashboard')


            else:

                return render(
                    request,
                    'users/login.html',
                    {
                        'error': 'Invalid password'
                    }
                )


        except User.DoesNotExist:

            return render(
                request,
                'users/login.html',
                {
                    'error': 'User does not exist'
                }
            )


    return render(
        request,
        'users/login.html'
    )


def dashboard(request):

    if 'user_id' not in request.session:

        return redirect('login')


    user = User.objects.get(
        id=request.session['user_id']
    )


    return render(
        request,
        'users/dashboard.html',
        {
            'user': user
        }
    )


def logout_view(request):

    request.session.flush()

    return redirect('home')