import csv

from ..models import Category, Comment, Genre, Review, Title, User


def user_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            _, created = User.objects.get_or_create(
                id=int(row[0]),
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6],
            )


def category_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            _, created = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )


def genre_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            _, created = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2],
            )


def title_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            category = Category.objects.get(pk=int(row[3]))
            _, created = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=int(row[2]),
                category=category,
            )


def review_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            title = Title.objects.get(pk=int(row[1]))
            author = User.objects.get(pk=int(row[3]))
            _, created = Review.objects.get_or_create(
                id=int(row[0]),
                title=title,
                text=row[2],
                author=author,
                score=int(row[4]),
                pub_date=row[5],
            )


def comment_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            review = Review.objects.get(pk=int(row[1]))
            author = User.objects.get(pk=int(row[3]))
            _, created = Comment.objects.get_or_create(
                id=int(row[0]),
                review=review,
                text=row[2],
                author=author,
                pub_date=row[4],
            )


def genre_title_parser(file):
    with open(file) as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            title = Title.objects.get(pk=int(row[1]))
            genre = Genre.objects.get(pk=int(row[2]))
            title.genre.add(genre)
