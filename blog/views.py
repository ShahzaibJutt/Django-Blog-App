from curses.ascii import HT
from urllib import request
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from blog_website.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


# Create your views here.

def home(request):
    postsdict = {
        'posts': Post.objects.all(),
    }
    return render(request, 'blog/home.html', postsdict)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = '-date_posted'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        subject = 'Django Blog Website - New Post Creation Notification'
        message = 'Your post has been uploaded to the blog'
        recepient = str(form.instance.author.email)
        send_mail(subject, message, EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        subject = 'Django Blog Website - Post Updated Notification'
        message = f'Your post has been updated.'
        recepient = str(form.instance.author.email)
        send_mail(subject, message, EMAIL_HOST_USER,
                  [recepient], fail_silently=False)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            subject = 'Django Blog Website - Post Deletion Notification'
            message = 'Your post has been deleted.'
            recepient = str(post.author.email)
            send_mail(subject, message, EMAIL_HOST_USER,
                      [recepient], fail_silently=False)
        return True
        return False


def about(request):
    return HttpResponse('<h1>About</h1>')
