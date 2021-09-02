import bcrypt
from django.shortcuts import render, redirect
from .models import Users, Posts, Comments
from django.contrib import messages
from .decorators import login_required

@login_required
def index(request):
    context = {
        'users' : Users.objects.all(),
        'posts' : Posts.objects.all().order_by('-created_at'),
    }
    return render(request, 'index.html', context)

@login_required
def wall(request):
    context = {
        'users' : Users.objects.all(),
        'posts' : Posts.objects.all().order_by('-created_at'),
        'comments' : Comments.objects.all()
    }
    return render(request, 'wall.html', context)

@login_required
def comment(request, message_id):
    comment = request.POST['comment']
    user_id = int(request.session['user']['id'])
    user = Users.objects.get(id = user_id)
    post = Posts.objects.get(id=message_id)
    new_comment = Comments.objects.create(comment = comment)
    post.comments.add(new_comment)
    user.comments.add(new_comment)

    context = {
        'posts' : Posts.objects.all().order_by('-created_at'),
        'post_comments' : Comments.objects.all(),
        'users' : Users.objects.all()
    }
    return render(request, 'wall.html', context)

@login_required
def new_message(request):
    user_id = int(request.session['user']['id'])
    user = Users.objects.get(id = user_id)
    post = str(request.POST['message'])
    # import pdb
    # pdb.set_trace()
    new_message = Posts.objects.create(post = post)
    user.posts.add(new_message)
    messages.success(request, "Message successfully created")

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def destroy_message(request, message_id):
    post = Posts.objects.get(id=message_id)
    post.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def destroy_comment(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, error_message in errors.items():
                messages.error(request, error_message)
            return redirect('/register')
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = Users.objects.create(first_name = first_name, last_name = last_name, email = email, password = password)
        
        request.session['user'] = {
            'id' : user.id,
            'name' : user.first_name,
            'email' : user.email
        }

        messages.success(request, 'User successfully registered')
        return redirect('../')


def login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = Users.objects.get(email = email)
    except Users.DoesNotExist:
        messages.error(request, 'The user or password does not exist')
        return redirect('/register')
    
    if  not bcrypt.checkpw(password.encode(), user.password.encode()): 
        messages.error(request, 'The user or password does not exist')
        return redirect('/register')
    
    request.session['user'] = {
        'id': user.id,
        'name': user.first_name,
        'email': user.email
    }

    messages.success(request, f'Welcome {user.first_name}')
    return redirect('../')


def logout(request):
    del request.session['user']
    return redirect('/register')