from django.shortcuts import render, redirect
from .forms.user import UserForm, UserLoginForm
from django.contrib import messages
from wall_app.models import *
from datetime import datetime, timezone, timedelta
from django.http import HttpResponse, JsonResponse
# Create your views here.

def index(request):
    context = {
        'msgs' : Message.objects.all()
    }
    return render(request, 'wall_app/index.html', context)

def add_message(request):
    if request.method == 'GET':
        return redirect('wall')

    if request.method == 'POST':
        errors = Message.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = User.objects.get(email=request.session['logged_user'])
            message = Message(message=request.POST['message'], user=user)
            message.save()

        return redirect('wall')

def add_message_ajax(request):
    if request.method == 'GET':
        return redirect('wall')

    if request.method == 'POST':
        errors = Message.objects.validator(request.POST)
        if len(errors) > 0:
            values = ''
            for key, value in errors.items():
                values += value + '\n'
            return JsonResponse({'alert' : values})
        else:
            user = User.objects.get(email=request.session['logged_user'])
            message = Message(message=request.POST['message'], user=user)
            message.save()

        return JsonResponse({'alert' : 'Mensaje agregado!'})

def add_comment(request):
    if request.method == 'GET':
        return redirect('wall')

    if request.method == 'POST':
        errors = Comment.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = User.objects.get(email=request.session['logged_user'])
            message = Message.objects.get(id=int(request.POST['id_message']))
            comment = Comment(comment=request.POST['comment'], message=message, user=user)
            comment.save()
        
        return redirect('wall')

def add_comment_ajax(request):
    if request.method == 'GET':
        return redirect('wall')

    if request.method == 'POST':
        errors = Comment.objects.validator(request.POST)
        if len(errors) > 0:
            values = ''
            for key, value in errors.items():
                values += value + '\n'
            return JsonResponse({'alert' : values})
        else:
            user = User.objects.get(email=request.session['logged_user'])
            message = Message.objects.get(id=int(request.POST['id_message']))
            comment = Comment(comment=request.POST['comment'], message=message, user=user)
            comment.save()
        
        return JsonResponse({'alert' : 'Comentario agregado!'})

def delete_comment(request, id_comment):
    comments = Comment.objects.filter(id=id_comment)
    if len(comments) != 1:
        messages.error(request, 'comentario no existe')
        return redirect('wall')
    comment = comments[0]
    if comment.user.email != request.session['logged_user']:
        messages.error(request, 'comentario es de otro usuario')
        return redirect('wall')

    now = datetime.now(timezone.utc)
    diif = now - comment.created_at
    seconds = diif.seconds
    minutes = (seconds / 60)
    
    if int(minutes) > 30:
        messages.error(request, f'Comentario ya no se puede eliminar')
        return redirect('wall')

    if comment.delete():
        messages.error(request, 'comment eliminado!')
        return redirect('wall')

def delete_comment_ajax(request, id_comment):
    comments = Comment.objects.filter(id=id_comment)
    if len(comments) != 1:
        return JsonResponse({'alert' : 'Comentario no existe'})
    comment = comments[0]
    if comment.user.email != request.session['logged_user']:
        return JsonResponse({'alert' : 'Comentario es de otro usuario'})

    now = datetime.now(timezone.utc)
    diif = now - comment.created_at
    seconds = diif.seconds
    minutes = (seconds / 60)
    
    if int(minutes) > 30:
        return JsonResponse({'alert' : 'Comentario ya no se puede eliminar'})

    if comment.delete():
        return JsonResponse({'alert' : 'Comentario eliminado!'})

def delete_msg(request, id_msg):
    msgs = Message.objects.filter(id=id_msg)
    if len(msgs) != 1:
        messages.error(request, 'Mensaje no existe')
        return redirect('wall')
    msg = msgs[0]
    if msg.user.email != request.session['logged_user']:
        messages.error(request, 'mensaje es de otro usuario')
        return redirect('wall')

    now = datetime.now(timezone.utc)
    diif = now - msg.created_at
    seconds = diif.seconds
    minutes = (seconds / 60)
    
    if int(minutes) > 30:
        messages.error(request, f'Mensaje ya no se puede eliminar')
        return redirect('wall')

    if msg.delete():
        messages.error(request, 'Mensaje eliminado!')
    return redirect('wall')

def delete_msg_ajax(request, id_msg):
    print(id_msg)
    msgs = Message.objects.filter(id=id_msg)
    if len(msgs) != 1:
        return JsonResponse({'alert' : 'Mensaje no existe'})
    msg = msgs[0]
    if msg.user.email != request.session['logged_user']:
        return JsonResponse({'alert' : 'mensaje es de otro usuario'})

    now = datetime.now(timezone.utc)
    diif = now - msg.created_at
    seconds = diif.seconds
    minutes = (seconds / 60)
    
    if int(minutes) > 30:
        return JsonResponse({'alert' : 'Mensaje ya no se puede eliminar'})

    if msg.delete():
        return JsonResponse({'alert' : 'mensaje eliminado!'})

def register(request):
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm()
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        print('va a register nuevo')
        return render(request, 'wall_app/register.html', context)
    
    if request.method == 'POST':
        print(request.POST)
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, 'wall_app/register.html', context)

        if User.ifExists(request.POST['email']):
            messages.error(request, 'Usuario ya existe')
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, 'wall_app/register.html', context)

        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            request.session['logged_user'] = user.email
        else:
            context = {
                'user_form' : UserForm(request.POST),
                'user_login_form' : UserLoginForm(),
            }
            return render(request, 'wall_app/register.html', context)

    return redirect('wall')

def login(request):
    print(request.POST)
    if request.method == 'GET':
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
            }
        return render(request, 'wall_app/register.html', context)

    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        if loginForm.is_valid():
            logged_user = loginForm.login(request.POST)
            if logged_user:
                request.session['logged_user'] = logged_user.email
                print('logged_user: ', request.session['logged_user'])
                return redirect('wall')
            
        user_form = UserForm()
        user_login_form = UserLoginForm(request.POST)
        context = {
            'user_form' : user_form,
            'user_login_form' : user_login_form,
        }
        return render(request, 'wall_app/register.html', context)

def logout(request):
    try:
        del request.session['logged_user']
    except:
        print('Error')
    return redirect('wall')
