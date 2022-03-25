from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import (Category, Comment, Genre, Review, Title, User,
                            UserRole)


class RegistrationSerializer(serializers.Serializer):
    username = serializers.SlugField(
        required=True,
    )
    email = serializers.EmailField(
        max_length=255,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            raise serializers.ValidationError(
                'выберите другое username, недопустипмо использовать "me"')
        return User.objects.create(**validated_data)


class MyTokenObtainSerializer(serializers.Serializer):
    username = serializers.SlugField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=255,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        max_length=150,
        required=False
    )
    last_name = serializers.CharField(
        max_length=150,
        required=False
    )
    bio = serializers.CharField(
        required=False
    )
    role = serializers.ChoiceField(
        choices=UserRole.ROLE_CHOICE,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def create(self, validated_data):
        if validated_data['username'] == 'me':
            raise serializers.ValidationError(
                'выберите другое username, недопустипмо использовать "me"')
        return User.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField()
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=serializers.Field())

    class Meta:
        model = Review
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]

    def validate_title(self, value):
        title_id = self.context['view'].kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        exclude = ('review',)
