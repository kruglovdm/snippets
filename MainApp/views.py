from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', "snippet_form": form}
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list")



def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', "snippets": snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    snippet = Snippet.objects.get(pk=snippet_id)
    context = {'pagename': 'Страница сниппета', "snippet": snippet}
    return render(request, 'pages/snippet_page.html', context)