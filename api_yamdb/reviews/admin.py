from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role'
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'category', 'genres']

    def genres(self, obj):
        return "\n".join([a.name for a in obj.genre.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'score', 'pub_date']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'author', 'pub_date']


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
