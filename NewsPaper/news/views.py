from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .forms import PostForm, BaseRegisterForm
from .models import Post
from .filters import PostFilter
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin


# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'


class AllPostsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllPostsList, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class SearchPostList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleList(ListView):
    queryset = Post.objects.filter(post_type='AR').order_by('creation_time')
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostView(DetailView):
    # queryset = Post.objects.filter(post_type='AR').order_by('creation_time')
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsList(ListView):
    queryset = Post.objects.filter(post_type='NW').order_by('creation_time')
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class NewsView(DetailView):
    queryset = Post.objects.filter(post_type='NW')
    template_name = 'detail_news.html'
    context_object_name = 'news'


class ArticleView(DetailView):
    queryset = Post.objects.filter(post_type='AR')
    template_name = 'article.html'
    context_object_name = 'article'


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        return super().form_valid(form)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "NW":
            raise Http404('Такой новости нет!')
        return super(NewsUpdate, self).dispatch(
            request, *args, **kwargs)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_news')
    permission_required = ('news.delete_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "NW":
            raise Http404('Такой новости нет!')
        return super(NewsDelete, self).dispatch(
            request, *args, **kwargs)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "AR":
            raise Http404('Такой статьи нет!')
        return super(ArticleUpdate, self).dispatch(
            request, *args, **kwargs)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_articles')
    permission_required = ('news.delete_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "AR":
            raise Http404('Такой статьи нет!')
        return super(ArticleDelete, self).dispatch(
            request, *args, **kwargs)


@login_required
def become_an_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')

# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/posts/')
#     return render(request, 'post_edit.html', {'form': form})
