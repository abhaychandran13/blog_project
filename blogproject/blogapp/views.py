from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm


def home(request):
    return render(request, "login.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('blogapp:viewall', pk=1)
        else:
            messages.error(request, "Invalid username or password")
            return redirect('blogapp:login')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already in use")
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,
                                                password=password)
                user.save();
                messages.success(request, "User registered successfully")
                return redirect('blogapp:login')
        else:
            messages.error(request, "Incorrect Password")
    return render(request, "registration.html")


def submit(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Create a new post with the form data
            new_post = form.save(commit=False)
            new_post.author = request.user  # Set the author to the logged-in user
            new_post.save()
            return redirect('blogapp:myblogs')  # Redirect to the post list page
    else:
        form = PostForm()

    return render(request, 'submit.html', {'form': form})


def viewall(request, pk):
    posts = Post.objects.order_by('-pub_date')

    return render(request, 'viewall.html', {'posts': posts})


def myblogs(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    return render(request, 'myblogs.html', {'posts': posts})


def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return HttpResponse("You don't have permission to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blogapp:myblogs')
    else:

        form = PostForm(instance=post)

    return render(request, 'update.html', {'form': form, 'Post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author:

        post.delete()

        return redirect('blogapp:myblogs')
    else:

        return HttpResponse("You don't have permission to delete this post.")


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        author = request.user
        comment = Comment(post=post, author=author, content=content)
        comment.save()

    return redirect('blogapp:post_detail', post_id=post_id)


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect('blogapp:post_detail', post_id=post_id)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            messages.success(request, "Comment added successfully.")

            return redirect('blogapp:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    comments = post.comment_set.all()

    return render(request, 'post_detail.html', {'form': form, 'post': post, 'comments': comments})


def logout(request):
    auth.logout(request)
    return redirect('/')
