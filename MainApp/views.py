from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth
from django.core.exceptions import ValidationError


def index_page(request):
    context = {
        'page_id': 'home',
        'pagename': 'PythonBin',
    }
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'page_id': 'add_snippet',
            'pagename': 'Добавление нового сниппета',
            "form": form}
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect("snippets-list")



def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'page_id': 'view_snippets',
        'pagename': 'Просмотр сниппетов',
        "snippets": snippets,
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    context = {
        'page_id': 'snippet_page',
        'pagename': 'Страница сниппета',
        "snippet": snippet}
    return render(request, 'pages/snippet_page.html', context)

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            raise ValidationError("Неправильный логин или пароль")
    return redirect('home')

def logout_page(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def reg_page(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            'page_id': 'registration',
            'pagename': 'Регистрация пользователя',
            "form": form}
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")


