from multiprocessing import context
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from requests import get
from reviews.forms import ReviewForm, CommentForm
from .models import Review, Comment
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    k = Review.objects.all().order_by("-id")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(k, 3)
    page_obj = paginator.get_page(page)
    context = {
        "v": k,
        "question_list": page_obj,
    }

    return render(request, "reviews/index.html", context)


def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews:index", review.pk)
    else:
        review_form = ReviewForm()
    context = {
        "create_form": review_form,
    }
    return render(request, "reviews/create.html", context)


def detail(request, pk):
    k = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = k.comment_set.all()
    context = {
        "i": k,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, "reviews/detail.html", context)


def delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect("reviews:index")
    return redirect("reviews:detail", review.pk)


def update(request, pk):
    k = get_object_or_404(Review, pk=pk)
    if request.user == k.user:
        if request.method == "POST":
            review_form = ReviewForm(request.POST, request.FILES, instance=k)
            if review_form.is_valid():
                review_form.save()
                return redirect("reviews:index", k.pk)
        else:
            review_form = ReviewForm(instanc=k)
        context = {
            "review_form": review_form,
            "k": k,
        }
        return render(request, "reviews/update.html", context)


def comment_create(request, article_pk):
    article = Review.objects.get(pk=article_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
            messages.success(request, "댓글 추가 완료")
    else:
        messages.warning(request, "잘못된 접근입니다.")
    return redirect("reviews:detail", article.pk)


def comment_update(request, article_pk, comment_pk):
    article = Review.objects.get(pk=article_pk)
    comment = Comment.objects.get(pk=comment_pk)

    if request.user != comment.user:
        messages.warning(request, "권한이 없습니다.")
        return redirect("reviews:detail", article.pk)

    if request.method == "POST":
        updated_comment = request.POST.get("updated_comment")
        if 0 < len(updated_comment) <= 80:
            comment.content = updated_comment
            comment.article = article
            comment.save()
            messages.success(request, "댓글 수정 완료")
    else:
        messages.warning(request, "잘못된 접근입니다.")
    return redirect("reviews:detail", article.pk)


def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user != comment.user:
        messages.warning(request, "권한이 없습니다.")
        return redirect("reviews:detail", article_pk)
    if request.method == "POST":
        comment.delete()
        messages.warning(request, "댓글 삭제 완료")
    else:
        messages.warning(request, "잘못된 접근입니다.")
    return redirect("reviews:detail", article_pk)
