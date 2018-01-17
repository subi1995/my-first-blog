from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

## 여기는 bootstrap 연결 test 
from django.http import HttpResponse
from django.template import loader

def home(request):
    return render(request, 'blog/home.html')

def photo(request):
    return render(request, 'blog/photo.html')


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# pk는 post 번호로 database prime? key 의 약자, 매개변수르 들어온다.

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# 새로운 postㄹ를 위한 view
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(request.POST, instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

## 여기는 bootstrap 연결 test
##def index(request):
##   template = loader.get_template('blog_bs/index.html')
##   context = {
##      'latest_question_list': "test",
##   }
##   return HttpResponse(template.render(context, request))
