from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Author, Category
from .filters import PostFilter, CategoryFilter
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin


# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'
from .templatetags.utils import new_post_nottification, check_posts_count


class AllPostsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllPostsList, self).get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['cat_filter'] = self.cat_filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.cat_filter = CategoryFilter(self.request.GET, queryset)
        return self.cat_filter.qs


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
        news.post_author = Author.objects.filter(username=self.request.user)[0]
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        check_posts_count(request)
        return super(NewsCreate, self).get(request, *args, *kwargs)

    # def post(self, request, *args, **kwargs):
    #     send_email('новость', request)
    #     return super(NewsCreate, self).post(request, *args, **kwargs)


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "NW":
            raise Http404('Такой новости нет!')
        elif str(self.request.user) != str(self.get_object().post_author):
            raise Http404("Только автор может вносить изменение в новость!")
        else:
            return super(NewsUpdate, self).dispatch(request, *args, **kwargs)


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_news')
    permission_required = ('news.delete_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "NW":
            raise Http404('Такой новости нет!')
        elif str(self.request.user) != str(self.get_object().post_author):
            raise Http404("Вы не автор данной новости!")
        else:
            return super(NewsDelete, self).dispatch(request, *args, **kwargs)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'AR'
        news.post_author = Author.objects.filter(username=self.request.user)[0]
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        check_posts_count(request)
        return super(ArticleCreate, self).get(request, *args, *kwargs)

    # def post(self, request, *args, **kwargs):
    #     send_email('статья', request)
    #     return super(ArticleCreate, self).post(request, *args, **kwargs)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "AR":
            raise Http404('Такой статьи нет!')
        elif str(self.request.user) != str(self.get_object().post_author):
            raise Http404("Только автор может вносить изменение в статью!")
        else:
            return super(ArticleUpdate, self).dispatch(request, *args, **kwargs)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_articles')
    permission_required = ('news.delete_post',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "AR":
            raise Http404('Такой статьи нет!')
        elif str(self.request.user) != str(self.get_object().post_author):
            raise Http404("Вы не автор данной статьи!")
        else:
            return super(ArticleDelete, self).dispatch(request, *args, **kwargs)


@login_required
def become_an_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    author = Author(username=user, nick_name=user)
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        author.save()
    return redirect('/')

@login_required
def subscribe(request):
    ref = request.META.get('HTTP_REFERER')
    if 'category' in ref:
        categories = ref.split('?')[1].split('&')
        user = User.objects.filter(username=request.user)
        print(user)
        for category in categories:
            cat = Category.objects.filter(pk=category.split('=')[1])[0]
            cat.subscribers.add(*user)
    return redirect(ref)


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
