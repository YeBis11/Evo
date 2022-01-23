from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Email, Message
from .forms import EmailForm


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'hello/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'hello/login_register.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    user = None
    try:
        user = User.objects.get(id=pk)
    except:
        pass

    emails = Email.objects.all()
    emails_messages = []

    for email in  emails:
        if str(user) == str(email.user):
            emails_messages.append(email)

    context = {'user': user, 'emails_messages': emails_messages}
    return render(request, 'hello/profile.html', context)


@login_required(login_url='login')
def index(request):
    form = EmailForm()
    context = {'form': form}
    return render(request, 'hello/hello.html', context)


@login_required(login_url='login')
def greet(request):
    greet_message = ''
    if request.method == 'POST':
        if request.POST:
            email = request.POST['email'].strip()
            form = EmailForm(request.POST)
            for item in Email.objects.all():
                if email == str(item):
                    greet_message = f'We already said hello to {email}!'
                    break
            if not greet_message:
                new_email = Email.objects.create(
                    user=request.user,
                    email=email,
                )
                greet_message = f'Hello, {email}!'
    context = {'greet_message': greet_message}
    return render(request, 'hello/greet.html', context)


@login_required(login_url='login')
def email(request):
    emails = Email.objects.all()
    emails_count = emails.count()

    emails_messages = Message.objects.all()

    context = {'emails': emails, 'emails_count': emails_count,
               'emails_messages': emails_messages}
    return render(request, 'hello/emails.html', context)


@login_required(login_url='login')
def show_email_info(request, pk):
    try:
        int(pk)
        Email.objects.get(id=pk)
    except:
        return redirect('email')

    email = Email.objects.get(id=pk)
    participants = email.participants.all()

    if request.method == 'POST':
        if request.POST['body']:
            message = Message.objects.create(
                user=request.user,
                email=email,
                body=request.POST.get('body')
            )
            email.participants.add(request.user)
            return redirect('show', pk=email.id)

    user_messages = email.message_set.all()

    context = {'email': email, 'conversation': user_messages,
               'participants': participants}
    return render(request, 'hello/show.html', context)


@login_required(login_url='login')
def update_email(request, pk):
    try:
        email = Email.objects.get(id=pk)
    except:
        return redirect('email')
    form = EmailForm(instance=email)

    if request.user != email.user:
        return HttpResponse("""<strong>You are not allowed here!<strong><br>
                            <a href="{% url 'email'%}"><button>Emails</button><a/>""")

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=email)
        if form.is_valid():
            form.save()
            return redirect('email')

    context = {'form': form}
    return render(request, 'hello/email_update.html', context)


@login_required(login_url='login')
def delete_email(request, pk):
    try:
        email = Email.objects.get(id=pk)
    except:
        return redirect('email')

    if request.user != email.user:
        return HttpResponse("""<strong>You are not allowed here!<strong><br>
                            <a href="{% url 'email'%}"><button>Emails</button><a/>""")

    if request.method == 'POST':
        email.delete()
        return redirect('email')

    context = {'obj': email}
    return render(request, 'hello/delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except:
        return redirect('email')

    if request.user != message.user:
        return HttpResponse("""<strong>You are not allowed here!<strong><br>
                            <a href="{% url 'show' email.id %}"><button>Show</button><a/>""")

    if request.method == 'POST':
        print(message.email.id)
        message.delete()
        return redirect('/email/show/' + str(message.email.id))

    context = {'obj': message}
    return render(request, 'hello/delete.html', context)
