from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse
#from datetime import datetime
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post_raiting = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum']*3
        author_comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        under_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']

        self.rating = author_post_raiting + author_comment_rating + under_post_comment_rating
        self.save()

        def __str__(self):
            return f"{self.authorUser}"


class Category(models.Model):
    category_name = models.CharField(max_length=80, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self) -> str:
        return self.category_name
    

class Post(models.Model):
    ARTICLES = 'AT'
    NEWS = 'NW'
    post_type_list = [
        (ARTICLES, 'Статья'), 
        (NEWS, 'Новость'),
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length = 2, choices = post_type_list, default = NEWS)
    create_time = models.DateTimeField(auto_now_add = True)
    post_title = models.CharField(max_length=80)
    post_text = models.TextField(default='место для вашей рекламы')
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.post_text) < 124:
            return self.post_text
        else:
            return self.post_text[:124] + '...'
        
    def __str__(self):
        dataf = 'Post from {}'.format(self.create_time.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.author},{self.post_title}"

    def __str__(self):
        return f'{self.post_title.title()}: {self.post_text[:10]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

   
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post}, from the category:  {self.category}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default='место для вашей рекламы')
    create_time = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.create_time}, {self.user}"