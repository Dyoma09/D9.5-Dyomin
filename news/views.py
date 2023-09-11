from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from .filters import NewsFilter
from .forms import NewsForm

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

class AuthorList(ListView):
    model = Author
    context_object_name = 'Author'

class ListNews(ListView):
    model = Post
    ordering = 'post_title'
    template_name = 'news_test.html'
    context_object_name = 'news_list'
   
    queryset = Post.objects.filter(post_type='NW').order_by('-id')

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    Author.objects.create(user=user)
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    return redirect('/news/')
    
class ListNewsSearch(ListView):
    model = Post
    ordering = 'post_title'
    template_name = 'news_search_test.html'
    context_object_name = 'news_search'

    paginate_by = 5

    def get_queryset(self):
       
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    
class DetailNews(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'


class CreateNews(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        return super().form_valid(form)
    



class UpdateNews(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.change_post', )


class DeleteNews(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AT'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_create.html'
    permission_required = ('news.change_post', )


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

def error_403(request, exception):
    return render(request, 'errors/403.html')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'


    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

    
