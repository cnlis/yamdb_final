from django.core.management.base import BaseCommand

from ...parsers.csv_parsers import (category_parser, comment_parser,
                                    genre_parser, genre_title_parser,
                                    review_parser, title_parser, user_parser)


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = 'static/data'
        user_parser(f'{path}/users.csv')
        category_parser(f'{path}/category.csv')
        genre_parser(f'{path}/genre.csv')
        title_parser(f'{path}/titles.csv')
        review_parser(f'{path}/review.csv')
        comment_parser(f'{path}/comments.csv')
        genre_title_parser(f'{path}/genre_title.csv')
