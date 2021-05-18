from django.shortcuts import render, redirect
from django.contrib import messages
from shows.models import *
from . import show_maker
from django.http import HttpResponse, JsonResponse
from .forms.shows.show import ShowForm
from .forms.shows.user import UserForm, UserLoginForm

def digito_verificador(rut):
    reversed_digits = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    return (-s) % 11
    
def checkEmail(request):
    print(request.POST)
    errors = Shows.objects.checkEmail(request.POST['email'])
    print('errors: ',errors)
    return JsonResponse({'errors' : errors})

def okay(request):
    return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')

def index(request):
    return redirect('register')

def shows(request):
    if 'logged_user' not in request.session:
        return redirect('/')

    context = {
        'shows' : Shows.objects.all()
    }
    return render(request, 'shows/index.html', context)

def new_show(request):
    if 'logged_user' not in request.session:
        return redirect('/')

    return render(request, 'shows/new_show.html')

def show_show(request, id):
    if 'logged_user' not in request.session:
        return redirect('/')

    show = Shows.objects.filter(id=id)
    context = {
        'show' : show[0] if len(show) > 0 else show
    }
    return render(request, 'shows/show_show.html', context)

def edit_show(request, id):
    if 'logged_user' not in request.session:
        return redirect('/')

    show = Shows.objects.filter(id=id)
    print(show[0].release_date)
    context = {
        'show' : show[0] if len(show) > 0 else show
    }
    return render(request, 'shows/edit_show.html', context)

def update_show(request, id):
    if 'logged_user' not in request.session:
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'shows/edit_show.html')
    if request.method == 'POST':
        errors = Shows.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print(request.POST)
            context = {
                'show' : request.POST
            }
            return render(request, 'shows/edit_show.html', context)

    Shows.objects.filter(id=id).update(title=request.POST['title'])
    Shows.objects.filter(id=id).update(network=request.POST['network'])
    Shows.objects.filter(id=id).update(email=request.POST['email'])
    Shows.objects.filter(id=id).update(release_date=request.POST['release_date'])
    Shows.objects.filter(id=id).update(description=request.POST['description'])
    return redirect('/')

def delete_show(request, id):
    #Shows.objects.all().delete()
    if 'logged_user' not in request.session:
        return redirect('/')

    if request.method == 'GET':
        delete = Shows.objects.filter(id=id).delete()
        if delete[0] == 1:
            messages.error(request, f'se elimino show {id}')
        return redirect('/')
    if request.method == 'POST':
        return redirect('/')

def create_show(request):
    if 'logged_user' not in request.session:
        return redirect('/')

    if request.method == 'GET':
        show_form = ShowForm() 
        return render(request, 'shows/new_show.html', {'show_form' : show_form})

    if request.method == 'POST':
        errors = Shows.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print(request.POST)
            context = {
                'new_show' : request.POST
            }
            return render(request, 'shows/new_show.html', context)

        print('POST: ',request.POST)
        # PASO TODAS LAS VALIDACIONES, SE CREA NUEVO REGISTRO
        Shows.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=request.POST['release_date'], description=request.POST['description'])
        show = ShowsForm(request.POST)

    return redirect('/')

def register(request):
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm()
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        print('va a register nuevo')
        return render(request, 'shows/register.html', context)
    
    if request.method == 'POST':
        print(request.POST)
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {
                'user_form' : UserForm(request.POST)
            }
            return render(request, 'shows/register.html', context)

        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()

    return redirect('/')

def login(request):
    print(request.POST)
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
            }
        return render(request, 'shows/register.html', context)

    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            logged_user = loginForm.login(request.POST)
            if logged_user:
                request.session['logged_user'] = logged_user.email
                print('logged_user: ', request.session['logged_user'])
                return redirect('shows')
            
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        return render(request, 'shows/register.html', context)
        
def logout(request):
    try:
        del request.session['logged_user']
    except:
        print('Error')
    return redirect('/')

def make_data(request):
	show_maker.create_shows()
	return redirect('/')

    