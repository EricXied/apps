from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature, Post, SaveFileField
from .form import SavedFileInDjangoForm
from .chatbot.chat import get_response
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings


def index(request):
    features = Feature.objects.all()
    return render(request, "index.html", {"features": features})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Used")
                return redirect("register")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Used")
                return redirect("register")

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                return redirect("login")
        else:
            messages.info(request, "Password Not The Same")
            redirect("register")
    else:
        return render(request, "register.html")


def counter(request):
    posts = [1, 2, 3, 4, 5, "tim", "tom", "john"]

    return render(request, "counter.html", {"posts": posts})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect("/post")
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/post")


def post(request):
    if request.method == "POST":
        upload_file = request.FILES.get("upload-file")
        # print(upload_file)
        title = request.POST["title"]
        body = request.POST["body"]
        file_name = None
        save_file_form = SavedFileInDjangoForm(request.POST, request.FILES)

        if save_file_form.is_valid():
            post_file = request.FILES.get("upload-file")
            save_file_model = SaveFileField()
            save_file_model.save_file = post_file
            save_file_model.save()

            file_name = post_file.name

        Post.objects.create(title=title, body=body, file_data=file_name)
        return redirect("post")
    posts = Post.objects.all()
    return render(request, "post.html", {"posts": posts})


def article(request, pk):
    post = Post.objects.get(id=pk)
    ipynb = None
    if post.file_data:
        file_path = post.file_data

    return render(
        request,
        "article.html",
        {"post": post, "file_path": file_path, "MEDIA_URL": settings.MEDIA_URL},
    )


def del_article(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect("post")


@csrf_exempt
def predict(request):
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))
        response = get_response(post_data["message"])
        message = {"answer": response}

        return JsonResponse(message)
