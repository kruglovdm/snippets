from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.contrib import auth
from django.core.exceptions import ValidationError
from  django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {
        'page_id': 'home',
        'pagename': 'PythonBin',
    }
    return render(request, 'pages/index.html', context)


@login_required
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
            if not request.user:
                new_post.user = AnonymousUser
            else:
                new_post.user = request.user
            new_post.save()
            return redirect("snippets-list")


def snippets_page(request):

        if request.user.is_authenticated:
            snippets = Snippet.objects.all().filter(Q(public=1) | Q(user=request.user))
        else:
            snippets = Snippet.objects.all().filter(public=1)
        context = {
            'page_id': 'view_snippets',
            'pagename': 'Просмотр сниппетов',
            "snippets": snippets,
        }
        return render(request, 'pages/view_snippets.html', context)


def snippets_page_my(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'page_id': 'view_snippets',
        'pagename': 'Просмотр сниппетов',
        "snippets": snippets,
    }
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    if request.method == "GET":
        context = {
            'page_id': 'snippet_page',
            'pagename': 'Страница сниппета',
            "snippet": snippet}
        return render(request, 'pages/snippet_page.html', context)
    elif request.method == "POST":
        if 'dl' in request.POST:
            snippet.delete()
            return redirect("snippets-list")
        elif 'upd' in request.POST:
            form = SnippetForm(instance=snippet)
            context = {
                'page_id': 'snippet_page',
                'pagename': 'Редактирование сниппета',
                "form": form}
            return render(request, 'pages/add_snippet.html', context)
        elif 'sv' in request.POST:
            form = SnippetForm(request.POST, instance=snippet)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect("snippets-list")

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
    return redirect('home')
    #return redirect(request.META.get('HTTP_REFERER', '/'))

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


