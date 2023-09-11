import django_filters.widgets
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter
from django_filters.widgets import DateRangeWidget
from .models import Post



class NewsFilter(FilterSet):
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )

    create_time = DateFromToRangeFilter(
        widget=DateRangeWidget(attrs={'placeholder': 'ГГГГ.ММ.ДД'}),
        lookup_expr='gt',
        label='За период'
    )

    post_title = CharFilter(
        field_name='post_title',
        lookup_expr='icontains',
        label='Название'
    )

    class Meta:
        model = Post
        fields = {'post_title'}