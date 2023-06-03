from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=255, blank=True)
    user_rate = models.FloatField(default=0.0)

    def update_rating(self) -> None:
        com_rate = self.return_rate(Comment.objects.filter(user=self.pk).values('rate'), 'rate')
        post_rate = self.return_rate(Post.objects.filter(post_author=self.pk).values('rate'), 'rate')
        auth_posts = Post.objects.filter(post_author=self.pk).values('pk')
        sum_rate = 0
        for post in auth_posts:
            sum_rate += self.return_rate(Comment.objects.filter(to_post_id=post['pk']).values('rate'), 'rate')
        self.user_rate = com_rate + post_rate * 3 + sum_rate
        self.save()

    @staticmethod
    def return_rate(rate_list: list, key: str) -> int:
        sum_rate = 0
        for rate in rate_list:
            sum_rate += rate[key]
        return sum_rate


    def __str__(self):
        if self.nick_name:
            return f'{self.nick_name}'
        else:
            return f'{self.username}'


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.category}'


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_TYPE = [
        (article, 'Статья'),
        (news, 'Новости')
    ]
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=news)
    category = models.ManyToManyField(Category, through='PostCategory')
    rate = models.IntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True)

    def preview(self) -> None:
        return self.text[:124] + '...'

    def like(self) -> None:
        self.rate += 1
        self.save()

    def dislike(self) -> None:
        self.rate -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.text[:50]}...'

    def get_absolute_url(self):
        if self.post_type == "NW":
            return reverse('news', args=[str(self.id)])
        return reverse('article', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.post_type == 'NW':
            cache.delete(f'news-{self.pk}')
        else:
            cache.delete(f'article-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}:{self.post}'


class Comment(models.Model):
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)

    def like(self) -> None:
        self.rate += 1
        self.save()

    def dislike(self) -> None:
        self.rate -= 1
        self.save()

    def __str__(self):
        return f'{self.text}, @{self.user}'

