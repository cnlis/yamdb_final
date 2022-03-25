import django_filters as df

from reviews.models import Title


class TitleFilter(df.FilterSet):
    genre = df.CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = df.CharFilter(field_name='category__slug', lookup_expr='exact')
    year = df.NumberFilter(field_name='year', lookup_expr='exact')
    name = df.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
