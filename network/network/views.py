# views.py
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
import json
from .models import Post
User = get_user_model()


@login_required
def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)
    posts = profile_user.posts.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj
    })

@login_required
@csrf_exempt
def toggle_follow(request, user_id):
    if request.method == "POST":
        profile_user = get_object_or_404(User, pk=user_id)
        if profile_user != request.user:
            if request.user in profile_user.followers.all():
                profile_user.followers.remove(request.user)
            else:
                profile_user.followers.add(request.user)
        return HttpResponseRedirect(reverse("profile", args=[user_id]))


@csrf_exempt
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))

def all_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/all_posts.html", {
        "page_obj": page_obj
    })


@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({
            "success": True,
            "likes_count": post.likes.count(),
            "liked": liked
        })
    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def following(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    paginator = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        content = data.get('content', '')

        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                post.content = content
                post.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=403)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)