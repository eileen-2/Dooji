from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm, TagForm
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked'] = self.object.like_set.filter(user=self.request.user, is_deleted=False).exists()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.blog.pk})


class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        comment = self.get_object()
        comment.is_deleted = True
        comment.save()
        comment.replies.update(is_deleted=True)
        return reverse_lazy('blog:blog_detail', kwargs={'pk': comment.blog.pk})


class LikeCreateView(LoginRequiredMixin, CreateView):
    model = Like
    fields = []

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'pk': self.object.blog.pk})

    def form_valid(self, form):
        blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        like, created = Like.objects.get_or_create(Post=blog, user=self.request.user)
        if not created:
            like.is_deleted = not like.is_deleted
            like.save()
        return super().form_valid(form)