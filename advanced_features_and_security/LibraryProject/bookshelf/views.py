from django.shortcuts import render

# Create your views here.



# content/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Article


@permission_required("content.can_view", raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, "content/article_list.html", {"articles": articles})


@permission_required("content.can_create", raise_exception=True)
def article_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        Article.objects.create(title=title, body=body, owner=request.user)
        return redirect("article_list")
    return render(request, "content/article_create.html")


@permission_required("content.can_edit", raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.title = request.POST.get("title")
        article.body = request.POST.get("body")
        article.save()
        return redirect("article_list")
    return render(request, "content/article_edit.html", {"article": article})


@permission_required("content.can_delete", raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect("article_list")
