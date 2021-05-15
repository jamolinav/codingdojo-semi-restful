from django.shortcuts import render, redirect
from django.contrib import messages
from shows.models import *
from . import show_maker
from django.http import HttpResponse, JsonResponse

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

# Create your views here.
def index(request):
    #Shows.objects.all().delete()
    context = {
        'shows' : Shows.objects.all()
    }
    return render(request, 'shows/index.html', context)

def new_show(request):
    return render(request, 'shows/new_show.html')

def show_show(request, id):
    show = Shows.objects.filter(id=id)
    context = {
        'show' : show[0]
    }
    return render(request, 'shows/show_show.html', context)

def create_show(request):
    if request.method == 'GET':
        return render(request, 'shows/new_show.html')

    if request.method == 'POST':
        errors = Shows.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            #for key, value in request.POST.items():
            print(request.POST)
            context = {
                'new_show' : request.POST
            }
            return render(request, 'shows/new_show.html', context)

        print('POST: ',request.POST)
        # PASO TODAS LAS VALIDACIONES, SE CREA NUEVO REGISTRO
        Shows.objects.create(title=request.POST['title'], network=request.POST['network'], release_date=request.POST['release_date'], description=request.POST['description'])
    return redirect('/')

def make_data(request):
	show_maker.create_shows()
	return redirect("/")

    