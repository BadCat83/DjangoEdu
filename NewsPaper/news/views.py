from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class AllPostsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2


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


class NewsView(DetailView):
    queryset = Post.objects.filter(post_type='NW')
    template_name = 'detail_news.html'
    context_object_name = 'news'


class ArticleView(DetailView):
    queryset = Post.objects.filter(post_type='AR')
    template_name = 'article.html'
    context_object_name = 'article'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'NW'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "NW":
            raise Http404('Такой новости нет!')
        return super(NewsUpdate, self).dispatch(
            request, *args, **kwargs)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_news')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "NW":
            raise Http404('Такой новости нет!')
        return super(NewsDelete, self).dispatch(
            request, *args, **kwargs)

class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.post_type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "AR":
            raise Http404('Такой статьи нет!')
        return super(ArticleUpdate, self).dispatch(
            request, *args, **kwargs)


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('all_articles')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().post_type != "AR":
            raise Http404('Такой статьи нет!')
        return super(ArticleDelete, self).dispatch(
            request, *args, **kwargs)

# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/posts/')
#     return render(request, 'post_edit.html', {'form': form})
